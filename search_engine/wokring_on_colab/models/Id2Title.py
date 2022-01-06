import os
import pandas as pd

ID2TITLE_PATH = '/content/drive/MyDrive/id2title.csv'

print("Start - setup id2title")
id2title_df = pd.read_csv(ID2TITLE_PATH)
id2title_df.columns = ['page_id', 'title']
id2title_dict = id2title_df.set_index('page_id')
id2title_dict = id2title_dict.to_dict()['title']
print("Finish- setup id2title")

def retrive_titles(articles):
    """
    Gets the number of page views that each of the provide wiki articles
        had in August 2021.

    Parameters:
    -----------
    articles: List. list of article ids and their score (id,score)

    Returns:
    -----------
    return: a list of titles and score:(id,score)

    """
    
    # TODO: change this so it gets only the ids and returns the names then merge with pandas

    res = list()
    keys = id2title_dict.keys()
    for id, score in articles:
        if id in keys:
            res.append((id2title_dict[id],score))
    return res
