from models.InvertedIndex import InvertedIndex
from data.DataRetrival import get_wiki
index = InvertedIndex(docs=get_wiki())
index.write('.', 'index')