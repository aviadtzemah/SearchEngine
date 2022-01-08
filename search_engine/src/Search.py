import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.SearchBody import search_body_df
from src.SearchTitle import search_title_df
from src.SearchAnchor import search_anchor_df
from src.Pagerank import get_pagerank_df
from src.Pageview import get_pageview_df
from models.Id2Title import get_titles_df


def weighted_search_df(query, body_weight=0.2, title_weight=0.2, anchor_weight=0.2, pagerank_weight=0.2,
                       pageviews_weight=0.2, N=100):
    """
  Gets the best 100 search results for a given query.
  
  Parameters:
  -----------
  query: String. The query one which to do the search.

  body_weight: float. The weight of the body results on the final search result.
  title_weight: float. The weight of the title results on the final search result.
  anchor_weight: float. The weight of the anchor texts results on the final search result.
  pagerank_weight: float. The weight of the pagerank results on the final search result.
  pageviews_weight: float. The weight of the pageviews results on the final search result.

  the default values for the weights are equals distribution amoung them.

  N: integer. How many results to return

  Returns:
  -----------
  return: a list of floats:
        list of PageRank scores that correrspond to the provided article IDs.
  """

    body_results = search_body_df(query)
    body_results['score'] = body_results['score'] * body_weight

    scaler = MinMaxScaler()  # assuming that using the same scaler won't make any problems

    title_results = search_title_df(query)
    title_results['score'] = scaler.fit_transform(
        title_results[['score']]) * title_weight  # normalizing the results and multiplying by the weight

    anchor_results = search_anchor_df(query)
    anchor_results['score'] = scaler.fit_transform(
        anchor_results[['score']]) * anchor_weight  # normalizing the results and multiplying by the weight

    search_result = body_results.add(title_results, fill_value=0).add(anchor_results, fill_value=0)

    article_ids = search_result.index.tolist()
    # adding pagerank score
    if pagerank_weight != 0:
        pageranks = get_pagerank_df(article_ids).rename(
            columns={'rank': 'score'})  # TODO: maybe just change the name of the col in its function?
        pageranks['score'] = scaler.fit_transform(pageranks[['score']]) * pagerank_weight
        search_result = search_result.add(pageranks)

    # adding pageviews score
    if pageviews_weight != 0:
        pageviews = get_pageview_df(article_ids).rename(
            columns={'views': 'score'})  # TODO: maybe just change the name of the col in its function?
        pageviews['score'] = scaler.fit_transform(pageviews[['score']]) * pageviews_weight
        search_result = search_result.add(pageviews)

    # getting the titles
    search_result = search_result.nlargest(N, 'score')
    article_ids = search_result.index.tolist()
    titles = get_titles_df(article_ids)
    search_result = pd.concat([search_result, titles], axis=1)  # adding the titles of the results

    return search_result[['title']].to_records(index=True)


def search_wiki(query):
    ''' Returns up to a 100 of best search results for the query.

    Parameters:
    -----------
    query: String. The query one which to do the search.

    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
  '''
    return weighted_search_df(query, 0.1, 0.7, 0.2, 0, 0)  # best weights
