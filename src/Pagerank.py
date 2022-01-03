import pandas as pd
import os
PAGE_RANK_PATH = os.path.join("..","data","data","page_ranks.csv")

def retrive_pagerank(article_ids):
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
    # loading the pagerank.csv into pandas dataframe
    pagerank_df = pd.read_csv(PAGE_RANK_PATH)
    pagerank_df.columns = ['page_id', 'rank']
    selected = pagerank_df[pagerank_df['page_id'].isin(article_ids)]
    selected = selected.set_index('page_id')  # TODO: check if this takes too much time
    return selected['rank'].reindex(article_ids).tolist()