import json
from time import time

from src.Search import weighted_search_df

with open('C:/Users/aviad/Desktop/queries_train.json', 'rt') as f:
    queries = json.load(f)

train_queries = [(k, v) for k, v in queries.items()][:20]
test_queries = [(k, v) for k, v in queries.items()][20:]


def average_precision(true_list, predicted_list, k=40):
    true_set = frozenset(true_list)
    predicted_list = predicted_list[:k]
    precisions = []
    for i, doc_id in enumerate(predicted_list):
        if doc_id in true_set:
            prec = (len(precisions) + 1) / (i + 1)
            precisions.append(prec)
    if len(precisions) == 0:
        return 0.0
    return round(sum(precisions) / len(precisions), 3)


def calculate_metrics_for_queries(queries_to_run, body_weight, title_weight, anchor_weight, pagerank_weight,
                                  pageviews_weight):
    qs_res = []
    for tup in queries_to_run:
        duration, ap = None, None
        t_start = time()
        try:
            res = weighted_search_df(tup[0], body_weight, title_weight, anchor_weight, pagerank_weight,
                                     pageviews_weight).tolist()  # .get(url + '/search', {'query': q}, timeout=35)
            pred_wids, _ = zip(*res)
            ap = average_precision(tup[1], pred_wids)
        except:
            pass
        qs_res.append(ap)

    return qs_res


# def grid_search(train_set):
#     for body_weight in range(1, 7):
#         for title_weight in range(1, 7-body_weight):
#             for anchor_weight in range(1, 7-body_weight-title_weight):
#                 for pagerank_weight in range(1, 7-body_weight-title_weight-anchor_weight):
#                     for pageviews_weight in range(1, 7-body_weight-title_weight-anchor_weight-pagerank_weight):
#                         if body_weight + title_weight + anchor_weight + pagerank_weight + pageviews_weight == 1:

def grid_search(train_set):
    best_weights = ()
    best_precision = 0
    for body_weight in range(11):
        print(f"i'm at {body_weight} main iteration")
        for title_weight in range(11):
            for anchor_weight in range(11):
                for pagerank_weight in range(11):
                    for pageviews_weight in range(11):
                        if body_weight + title_weight + anchor_weight + pagerank_weight + pageviews_weight == 10:
                            results = calculate_metrics_for_queries(train_set, body_weight/10, title_weight/10, anchor_weight/10,
                                                                    pagerank_weight/10, pageviews_weight/10)
                            avg_precision = round(sum(results) / len(results), 3)
                            if avg_precision > best_precision:
                                best_weights = (
                                body_weight, title_weight, anchor_weight, pagerank_weight, pageviews_weight)
                                best_precision = avg_precision

                                print(f"found new best: {best_weights}. with score: {best_precision}")
    return best_weights


best = grid_search(train_queries)
print(f'The best found is {best}.')

test_precision = calculate_metrics_for_queries(test_queries, best[0]/10, best[1]/10, best[2]/10, best[3]/10, best[4]/10)
print(f'The precision of the best weights found on the test set is: {round(sum(test_precision)/len(test_precision), 3)}')

# total_time = 0
# total_precision = 0
# for res in qs_res:
#     total_time += res[1]
#     total_precision += res[2]
#     print(f'for query "{res[0]}"')
#     print(f'took {res[1]} seconds')
#     print(f'avg precision is {res[2]}')
#     print('-------------------------------------------')
#
# print(f'average time for respons: {total_time / len(qs_res)} seconds')
# print(f'average map precision: {total_precision / len(qs_res)}')
