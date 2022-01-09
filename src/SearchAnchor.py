from binary_inverted_index_anchor_gcp import InvertedIndex
from models.BinarySearch import binary_search_anchor
from data.common import get_posting_gen_binary

# D:/University/Information Retrieval/Project/data_to_work_with/title_postings_gcp/
print("loading anchor index")
anchor_index = InvertedIndex.read_index(
    '/home/aviadsha/data/anchor_postings_gcp/', 'index')
print("finished loading anchor index")


def search_anchor_df(query):
    """
  same as search_title but returns a dateframe
  """
    return binary_search_anchor(query, anchor_index)


def search_anchor_wiki(query):
    """
    Gets all the results for a given query using binary ranking on the titles

    Parameters:
    -----------
    query: String. The query.

    Returns:
    -----------
    return: a list of all the search results, ordered from best to worst where
      each element is a tuple (wiki_id, title).
    """
    # TODO: change the index we are utilizing once there is one
    return binary_search_anchor(query, anchor_index).sort_values(by=['score'], ascending=False).to_records(
        index=True)  # TODO: does it matter if it's a rec array or do we need to make it a list?
