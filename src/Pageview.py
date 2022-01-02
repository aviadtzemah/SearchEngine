import os
import pandas as pd
import pickle

PAGE_VIEW_PATH = os.path.join("..","data","data","pageviews-202108-user.pkl")


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
    # read in the counter
    with open(PAGE_VIEW_PATH, 'rb') as f:
        wid2pv = pickle.loads(f.read())

    # loading the counter into a df
    pageviews_df = pd.DataFrame.from_dict(wid2pv, orient='index').reset_index()
    pageviews_df.columns = ['page_id', 'views']

    selected = pageviews_df[pageviews_df['page_id'].isin(article_ids)]
    selected = selected.set_index('page_id')  # TODO: check if this takes too much time
    return selected['views'].reindex(article_ids).tolist()