
# for tokenizing
import re
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)
stopwords_frozen = frozenset(stopwords.words('english'))


def tokenize(text):
    """
    This function aims in tokenize a text into a list of tokens. Moreover, it filter stopwords.

    Parameters:
    -----------
    text: string , represting the text to tokenize.

    Returns:
    -----------
    list of tokens (e.g., list of tokens).
    """
    list_of_tokens = [token.group() for token in RE_WORD.finditer(text.lower()) if
                      token.group() not in stopwords_frozen]
    return list_of_tokens



def get_posting_gen(index):
    """
    This function returning the generator working with posting list.

    Parameters:
    ----------
    index: inverted index
    """
    words, pls = zip(*index.posting_lists_iter1())
    return words, pls


def get_title(wiki_id):
    url = f"https://en.wikipedia.org/?curid={wiki_id}"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for title in soup.find_all('title'):
        return title.get_text()