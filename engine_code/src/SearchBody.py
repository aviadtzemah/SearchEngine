import time
from collections import Counter

from data.common import get_posting_gen, get_posting_tokens, tokenize
from inverted_index_body_gcp import InvertedIndex
# from models.InvertedIndex import generate_document_tfidf_matrix,generate_query_tfidf_vector
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import math

# /content/drive/MyDrive/postings_gcp/index.pkl
# D:/University/Information Retrieval/Project/data_to_work_with/postings_gcp/
print("loading body index")
body_index = InvertedIndex.read_index(
    '/home/aviadsha/data/correct_body_postings_gcp/', 'index')
# words, pls = get_posting_gen(body_index)
print("finished loading body index")


def generate_query_tfidf_vector(query_to_search, index, words):
    """
    Generate a vector representing the query. Each entry within this vector represents a tfidf score.
    The terms representing the query will be the unique terms in the index.

    We will use tfidf on the query as well.
    For calculation of IDF, use log with base 10.
    tf will be normalized based on the length of the query.

    Parameters:
    -----------
    query_to_search: list of tokens (str). This list will be preprocessed in advance (e.g., lower case, filtering stopwords, etc.').
                     Example: 'Hello, I love information retrival' --->  ['hello','love','information','retrieval']

    index:           inverted index loaded from the corresponding files.

    Returns:
    -----------
    vectorized query with tf idf scores
    """

    epsilon = .0000001
    total_vocab_size = len(words)
    Q = np.zeros((total_vocab_size))
    term_vector = list(words)
    counter = Counter(query_to_search)
    for token in np.unique(query_to_search):
        if token in index.posting_locs.keys():  # avoid terms that do not appear in the index.
            tf = counter[token] / len(query_to_search)  # term frequency divded by the length of the query
            df = index.df[token]
            idf = math.log(6348910 / (df + epsilon), 10)  # smoothing. the magic number is the amount of docs

            try:
                ind = term_vector.index(token)
                Q[ind] = tf * idf
            except:
                pass
    return Q


def get_candidate_documents_and_scores_tfidf(query_to_search, index, words, pls):
    """
    Generate a dictionary representing a pool of candidate documents for a given query. This function will go through every token in query_to_search
    and fetch the corresponding information (e.g., term frequency, document frequency, etc.') needed to calculate TF-IDF from the posting list.
    Then it will populate the dictionary 'candidates.'
    For calculation of IDF, use log with base 10.
    tf will be normalized based on the length of the document.

    Parameters:
    -----------
    query_to_search: list of tokens (str). This list will be preprocessed in advance (e.g., lower case, filtering stopwords, etc.').
                     Example: 'Hello, I love information retrival' --->  ['hello','love','information','retrieval']

    index:           inverted index loaded from the corresponding files.

    words,pls: generator for working with posting.
    Returns:
    -----------
    dictionary of candidates. In the following format:
                                                               key: pair (doc_id,term)
                                                               value: tfidf score.
    """
    candidates = {}
    for term in np.unique(query_to_search):
        if term in words:
            list_of_doc = pls[words.index(term)]
            if type(list_of_doc) is tuple:
                list_of_doc = [list_of_doc]
            normlized_tfidf = [(doc_id, tfidf) for doc_id, tfidf in
                               list_of_doc]

            for doc_id, tfidf in normlized_tfidf:
                candidates[(doc_id, term)] = candidates.get((doc_id, term), 0) + tfidf

    return candidates


def generate_document_tfidf_matrix(query_to_search, index, words, pls):
    """
    Generate a DataFrame `D` of tfidf scores for a given query.
    Rows will be the documents candidates for a given query
    Columns will be the unique terms in the index.
    The value for a given document and term will be its tfidf score.

    Parameters:
    -----------
    query_to_search: list of tokens (str). This list will be preprocessed in advance (e.g., lower case, filtering stopwords, etc.').
                     Example: 'Hello, I love information retrival' --->  ['hello','love','information','retrieval']

    index:           inverted index loaded from the corresponding files.

    words,pls: generator for working with posting.
    Returns:
    -----------
    DataFrame of tfidf scores.
    """

    total_vocab_size = len(index.posting_locs)
    candidates_scores = get_candidate_documents_and_scores_tfidf(query_to_search, index, words,
                                                                 pls)  # We do not need to utilize all document. Only the docuemnts which have corrspoinding terms with the query.

    unique_candidates = np.unique([doc_id for doc_id, freq in candidates_scores.keys()])
    D = np.zeros((len(unique_candidates), len(words)))
    D = pd.DataFrame(D)

    D.index = unique_candidates
    D.columns = words

    for key in candidates_scores:
        tfidf = candidates_scores[key]
        doc_id, term = key
        D.loc[doc_id][term] = tfidf
    return D


def search_body_df(query, N=100):
    """
  same as search_body but returns a dateframe
  """

    tokenized_query = tokenize(query)
    # TODO: can we assume pls is not empty?
    words, pls = get_posting_tokens(body_index, tokenized_query)

    D = postings_to_df(pls)
    Q = generate_query_tfidf_vector(tokenized_query, body_index, words)# getting the tfidf vector of the query # TODO make this more efficient
    results = cosine_similarity([Q], D)  # calculating the cosine similarity
    # adding the results as a new column to the matrix of the docs.
    # cause now we know what is the cossim score of each doc with the query
    D['score'] = results[0]

    if N == -1:  #
        return D[['score']]
    return D.nlargest(N, 'score')[['score']]  # returning the N largest values


def postings_to_df(postings):

    df = pd.DataFrame(postings[0][1], columns=['doc_id', postings[0][0]]).set_index('doc_id')
    for i in range(1, len(postings)):
        df = pd.concat([df, pd.DataFrame(postings[i][1], columns=['doc_id', postings[i][0]]).set_index('doc_id')], axis=1)

    return df.fillna(0)

def search_body_wiki(query, N=100):
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

    tokenized_query = tokenize(query)
    # TODO: can we assume pls is not empty?
    words, pls = get_posting_tokens(body_index, tokenized_query)

    D = postings_to_df(pls)
    Q = generate_query_tfidf_vector(tokenized_query, body_index, words)  # getting the tfidf vector of the query
    results = cosine_similarity([Q], D)  # calculating the cosine similarity
    # adding the results as a new column to the matrix of the docs.
    # cause now we know what is the cossim score of each doc with the query
    D['score'] = results[0]

    if N == -1:  #
        return D[['score']].sort_values(by=['score'], ascending=False).to_records(index=True)
    return D.nlargest(N, 'score')[['score']].to_records(index=True)  # returning the N largest values

    # return search_body_df(query, N).to_records(index=True)
    #
    # return []
    # # TODO: do we need to check when the query is empty or just gibberish?
    # print(words)
    # print(pls)
    # D = generate_document_tfidf_matrix(tokenized_query, body_index, words,
    #                                    pls)  # getting the tfidf matrix of the relevent docs
    # print(D)
    # Q = generate_query_tfidf_vector(tokenized_query, body_index, words)  # getting the tfidf vector of the query
    # results = cosine_similarity([Q], D)  # calculating the cosine similarity
    # # adding the results as a new column to the matrix of the docs.
    # # cause now we know what is the cossim score of each doc with the query
    # D['score'] = results[0]

    # if N == -1:  #
    #     return D[['score']].sort_values(by=['score'], ascending=False).to_records(index=True)
    # return D.nlargest(N, 'score')[['score']].to_records(index=True)  # returning the N largest values

    # return search_body_df(query, N).to_records(index=True)
