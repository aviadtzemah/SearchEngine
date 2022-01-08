
from data import ENV
from data.common import tokenize
import json
import os

TRAIN_PATH = os.path.join("..","data","train","queries_train.json")
def get_wiki_test()->dict:
    raise NotImplementedError


def get_wiki_train() -> dict:
    with open(TRAIN_PATH, 'r') as train_data:
        return json.load(train_data)


def mock_data(data):
    docs = {}
    for key in data:
      for doc_id in data[key]:
        if doc_id not in docs:
          docs[doc_id] = []
        docs[doc_id] += tokenize(key)
    return docs

def get_wiki():
    if ENV == "TEST":
        return get_wiki_test()
    else:
        return mock_data(get_wiki_train())


