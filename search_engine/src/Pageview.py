import os
import pandas as pd
import pickle

PAGE_VIEW_PATH = 'D:/University/InformationRetrieval/Project/data_to_work_with/pageviews-202108-user.pkl'

print("Start - Set up pageviews")
with open(PAGE_VIEW_PATH, 'rb') as f:
    wid2pv = pickle.loads(f.read())

# loading the counter into a df
pageviews_df = pd.DataFrame.from_dict(wid2pv, orient='index').reset_index()
pageviews_df.columns = ['page_id', 'views']
pageviews_dict = pageviews_df.set_index('page_id')
pageviews_dict = pageviews_dict.to_dict()['views']
print("Finished- Set up pageviews")


def get_pageview_df(article_ids):
    return pd.DataFrame({'page_id': article_ids, 'score': [pageviews_dict.get(key) for key in article_ids]}).set_index(
        'page_id')


def retrieve_pageviews(article_ids):
    """
    Gets PageRank values for a list of provided wiki article IDs.

    Parameters:
    -----------
    article_ids: List. list of article ids of which to return the page ranks of.

    Returns:
    -----------
    return: a list of floats:
          list of PageRank scores that correrspond to the provided article IDs.
    """
    return [pageviews_dict.get(key) for key in article_ids]
