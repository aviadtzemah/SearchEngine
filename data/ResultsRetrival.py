
from data import ENV
import json
import os

def get_wiki_test()->dict:
    raise NotImplementedError


def get_wiki_train() -> dict:
    with open(os.path.join("train","queries_train.json"), 'r') as train_data:
        return json.load(train_data)


def get_wiki():
    if ENV == "TEST":
        return get_wiki_test()
    else:
        return get_wiki_train()


data = get_wiki()
x=0