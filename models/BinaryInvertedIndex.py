from pathlib import Path
from collections import defaultdict,Counter
import pickle
from operator import itemgetter
from contextlib import closing
import operator
from itertools import islice,count
from models.MultiFileWriter import MultiFileWriter,MultiFileReader


TUPLE_SIZE = 4  # We're going to pack the doc_id and tf values in this
# many bytes.
TF_MASK = 2 ** 16 - 1  # Masking the 16 low bits of an integer

DL = {}  # We're going to update and calculate this after each document. This will be usefull for the calculation of AVGDL (utilized in BM25)


class BinaryInvertedIndex:
    def __init__(self, docs={}):
        """ Initializes the inverted index and add documents to it (if provided).
        Parameters:
        -----------
          docs: dict mapping doc_id to list of tokens
        """
        # stores document frequency per term
        self.df = Counter()
        # stores total frequency per term
        self.term_total = Counter()
        # stores posting list per term while building the index (internally),
        # otherwise too big to store in memory.
        self._posting_list = defaultdict(list)
        # mapping a term to posting file locations, which is a list of
        # (file_name, offset) pairs. Since posting lists are big we are going to
        # write them to disk and just save their location in this list. We are
        # using the MultiFileWriter helper class to write fixed-size files and store
        # for each term/posting list its list of locations. The offset represents
        # the number of bytes from the beginning of the file where the posting list
        # starts.
        self.posting_locs = defaultdict(list)

        for doc_id, tokens in docs.items():
            self.add_doc(doc_id, tokens)

    def add_doc(self, doc_id, tokens):
        """ Adds a document to the index with a given `doc_id` and tokens. It counts
            the tf of tokens, then update the index (in memory, no storage
            side-effects).
        """
        DL[(doc_id)] = DL.get(doc_id, 0) + (len(tokens))
        w2cnt = Counter(tokens)
        self.term_total.update(w2cnt)
        max_value = max(w2cnt.items(), key=operator.itemgetter(1))[1]
        # frequencies = {key: value/max_value for key, value in frequencies.items()}
        for w, cnt in w2cnt.items():
            self.df[w] = self.df.get(w, 0) + 1
            self._posting_list[w].append((doc_id, cnt))

    def write(self, base_dir, name):
        """ Write the in-memory index to disk and populate the `posting_locs`
            variables with information about file location and offset of posting
            lists. Results in at least two files:
            (1) posting files `name`XXX.bin containing the posting lists.
            (2) `name`.pkl containing the global term stats (e.g. df).
        """
        #### POSTINGS ####
        self.posting_locs = defaultdict(list)
        with closing(MultiFileWriter(base_dir, name)) as writer:
            # iterate over posting lists in lexicographic order
            for w in sorted(self._posting_list.keys()):
                self._write_a_posting_list(w, writer, sort=True)
        #### GLOBAL DICTIONARIES ####
        self._write_globals(base_dir, name)

    def _write_globals(self, base_dir, name):
        with open(Path(base_dir) / f'{name}.pkl', 'wb') as f:
            pickle.dump(self, f)

    def _write_a_posting_list(self, w, writer, sort=False):
        # sort the posting list by doc_id
        pl = self._posting_list[w]
        if sort:
            pl = sorted(pl, key=itemgetter(0))
        # convert to bytes
        b = b''.join([(int(doc_id)).to_bytes(TUPLE_SIZE, 'big')
                      for doc_id, tf in pl])
        # write to file(s)
        locs = writer.write(b)
        # save file locations to index
        self.posting_locs[w].extend(locs)

    def __getstate__(self):
        """ Modify how the object is pickled by removing the internal posting lists
            from the object's state dictionary.
        """
        state = self.__dict__.copy()
        del state['_posting_list']
        return state

    def posting_lists_iter1(self):
        """ A generator that reads one posting list from disk and yields
            a (word:str, [(doc_id:int, tf:int), ...]) tuple.
        """
        with closing(MultiFileReader()) as reader:
            for w, locs in self.posting_locs.items():
                # read a certain number of bytes into variable b
                b = reader.read(locs, self.df[w] * TUPLE_SIZE)
                posting_list = []
                # convert the bytes read into `b` to a proper posting list.

                for i in range(self.df[w]):
                    doc_id = int.from_bytes(b[i * TUPLE_SIZE:i * TUPLE_SIZE + 4], 'big')
                    #tf = int.from_bytes(b[i * TUPLE_SIZE + 4:(i + 1) * TUPLE_SIZE], 'big')
                    posting_list.append(doc_id)

                yield w, posting_list

    @staticmethod
    def read_index(base_dir, name):
        with open(Path(base_dir) / f'{name}.pkl', 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def delete_index(base_dir, name):
        path_globals = Path(base_dir) / f'{name}.pkl'
        path_globals.unlink()
        for p in Path(base_dir).rglob(f'{name}_*.bin'):
            p.unlink()