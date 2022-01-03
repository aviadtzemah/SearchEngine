from models.InvertedIndex import InvertedIndex
from models.BinaryInvertedIndex import InvertedIndex
from data.DataRetrival import get_wiki
index = InvertedIndex(docs=get_wiki())
index.write('.', 'index')

binary_index = InvertedIndex(docs=get_wiki())
binary_index.write('.','binindex')