import numpy as np
import pandas as pd
from data.common import tokenize, get_posting_gen


def get_candidate_documents_and_scores_binary(query_to_search, index, words, pls):
    """
    Generate a dictionary representing a pool of candidate documents for a given query. This function will go through every token in query_to_search
    and fetch the occuring docs. where it counts how many query terms appeard in each candidate
    Then it will populate the dictionary 'candidates.'

    Parameters:
    -----------
    query_to_search: list of tokens (str). This list will be preprocessed in advance (e.g., lower case, filtering stopwords, etc.').
                     Example: 'Hello, I love information retrival' --->  ['hello','love','information','retrieval']

    index:           inverted index loaded from the corresponding files.

    words,pls: generator for working with posting.
    Returns:
    -----------
    dictionary of candidates. In the following format:
                                                               key: doc_id
                                                               value: how many query terms appeard in the candidate
    """
    candidates = {}
    for term in np.unique(query_to_search):
        if term in words:
            list_of_doc = pls[words.index(term)]

            # we only need to count how many times each doc occured
            for candidate in list_of_doc:
                candidates[candidate] = candidates.get(candidate, 0) + 1

    return candidates


def binary_search(query, binary_index, word, pls):
    """
    Gets all the results for a given query using binary ranking on the index docs

    Parameters:
    -----------
    query: String. The query.

    index: The index on which to do the search

    Returns:
    -----------
    return: a list of all the search results, ordered from best to worst where
      each element is a tuple (wiki_id, title).
    """
    #word, pls = get_posting_gen(index)
    #bword, bpls = get_posting_gen(binary_index)
    candidates = get_candidate_documents_and_scores_binary(tokenize(query), binary_index, word, pls)

    # candidates_list =
    return pd.DataFrame.from_dict(candidates, orient='index').rename(columns={0: 'score'})

    #candidates_list = pd.DataFrame.from_dict(candidates, orient='index')
    #return candidates_list.sort_values(by=0, ascending=False)