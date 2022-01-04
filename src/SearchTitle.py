
from models import binary_index
from models.BinarySearch import binary_search
def searchtitle(query):
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
    # TODO: change the idnex we are utilizing once there is one
    return binary_search(query, binary_index).sort_values(by=['score'], ascending=False).to_records(
        index=True)  # TODO: does it matter if it's a rec array or do we need to make it a list?