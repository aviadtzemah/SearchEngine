from data.common import get_posting_gen, tokenize
from models import index
from models.InvertedIndex import generate_document_tfidf_matrix,generate_query_tfidf_vector
from sklearn.metrics.pairwise import cosine_similarity
def searchbody(query, N=100):
    """
    Gets the best N results for a given query using TFIDF and cosine similarity

    Parameters:
    -----------
    query: String. The query.

    N: Integer. How many documents to retrieve. By default N = 100.
     if N is -1 then returns everything found ordered from best to worst.

    Returns:
    -----------
    return: a list of up to N search results, ordered from best to worst where
      each element is a tuple (wiki_id, title).
    """

    words, pls = get_posting_gen(index)
    tokenized_query = tokenize(query)
    D = generate_document_tfidf_matrix(tokenized_query, index, words,
                                       pls)  # getting the tfidf matrix of the relevent docs
    Q = generate_query_tfidf_vector(tokenized_query, index)  # getting the tfidf vector of the query
    results = cosine_similarity([Q], D)  # calculating the cosine similarity

    # adding the results as a new column to the matrix of the docs.
    # cause now we know what is the cossim score of each doc with the query
    D['score'] = results[0]

    if N == -1:  #
        return D[['score']].sort_values(by=['score'], ascending=False).to_records(index=True)
    return D.nlargest(N, 'score')[['score']].to_records(index=True)  # returning the N largest values

    # return search_body_df(query, N).to_records(index=True)