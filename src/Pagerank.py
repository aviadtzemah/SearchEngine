import pandas as pd
import os

PAGE_RANK_PATH = '/home/aviadsha/data/pagerank.csv'

print("Start - setup pagerank")
pagerank_df = pd.read_csv(PAGE_RANK_PATH)
pagerank_df.columns = ['page_id', 'rank']
pagerank_dict = pagerank_df.set_index('page_id')
pagerank_dict = pagerank_dict.to_dict()['rank']
print("Finish- setup pagerank")


def get_pagerank_df(article_ids):
    return pd.DataFrame({'page_id': article_ids, 'score': [pagerank_dict.get(key) for key in article_ids]}).set_index(
        'page_id')


def retrieve_pagerank(article_ids):
    """
    Gets the number of page views that each of the provide wiki articles
        had in August 2021.

    Parameters:
    -----------
    article_ids: List. list of article ids of which to return the page views of.

    Returns:
    -----------
    return: a list of ints:
          list of page view numbers from August 2021 that correrspond to the
          provided list article IDs.
    """

    return [pagerank_dict.get(key) for key in article_ids]
