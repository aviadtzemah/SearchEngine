
# #from models import title__index
# #from models.BinaryInvertedIndex import BinaryInvertedIndex
# from binary_inverted_index_gcp import InvertedIndex
# from models.BinarySearch import binary_search
# from data.common import get_posting_gen

# # /content/drive/MyDrive/title_postings_gcp/index.pkl
# # D:/University/Information Retrieval/Project/data_to_work_with/title_postings_gcp/
# print("loading title index")
# title_index = InvertedIndex.read_index('/content/drive/MyDrive/title_postings_gcp/', 'index')
# word, pls = get_posting_gen(title_index)
# print("finished loading title index")

# def search_title_df(query):
#   """ 
#   same as search_title but returns a dateframe
#   """
#   return binary_search(query, title_index, word, pls)

# def search_title_wiki(query):
#     """
#     Gets all the results for a given query using binary ranking on the titles

#     Parameters:
#     -----------
#     query: String. The query.

#     Returns:
#     -----------
#     return: a list of all the search results, ordered from best to worst where
#       each element is a tuple (wiki_id, title).
#     """
#     # TODO: change the idnex we are utilizing once there is one
#     return binary_search(query, title_index, word, pls).sort_values(by=['score'], ascending=False).to_records(
#         index=True)  # TODO: does it matter if it's a rec array or do we need to make it a list?