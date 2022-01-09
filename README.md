# SearchEngine

SearchEngine is a Python server search engine for searching the english [wikipedia](https://www.wikipedia.org/) site.
## Run
```bash
python3 src/search_frontend.py
```
## APIs
Our code contains the following API's
- **GET**
    - **<base-url>/search?query=<q>** - get function for searching wikipedia using all supporting data retrieval methods. the result is limited to the top 100 views with (wiki_id, title).
    - **<base-url>/search_body?query=<q>** - get function for searching wikipedia using only the body content, the result is limited to the top 100 views with (wiki_id, title).
    - **<base-url>/search_title?query=<q>** - get function for searching wikipedia using only the title content, returning (wiki_id, title).
    - **<base-url>/search_anchor?query=<q>** - get function for searching wikipedia using only the title content, returning (wiki_id, title).
- **POST**
    - **<base-url>/get_pagerank** - gets the page rank of the list of pages provided in POST data
    - **<base-url>/get_pageviews** - gets the page views of the list of pages provided in POST data in August 2021.
## Code Structure
Our project contains the following modules and files.
- data - Folder holding the data and supporting data related functions.
- models - Folder containing common logics for all APIs and Indexing related functions.
- src - containing the main code and it's logics divided into different modules.

This code is based on the source code provided by BGU university.

## Functionality
We will go through the data-flow for each API.
- **Indexing**
    In order to run the code we had to create an indexing for the body title and anchor values. Each one of them was computed as follows:
    - *Body Index* - the search body index was calculated using the id's and body words. Those words were entred as a raw input and their value was their already calculated tf-idf score.
    - *Title Index* - the search title index was calculated using the title's words and id's. Those words were entred as a raw input with no value as we only wants to know if a word appears in the title or not.
    - *Anchor Index* - the search anchor index was calculated using the anchors words and id's. Those words first indexed and the file that was slected was the file related to the anchor and not the file the anchor's appears in.
- **Server StartUp**
    When running the run command the following procedures are occurring before the server start listening
    - Indexes for search-body, search-title,search-anchor are loaded into RAM memory.
    - Entire page-rank and page-views are loaded to the RAM memory.
    - Entire id2title.csv is loaded to the RAM memory.
- **Requests**
    - *GET-* **serach** - in search function (src/Search.py) we activate all of the following functions and logic to retrive all pf the relvamt files with all relevant methods, those results are prioritze using predetermined weights that are subjected into the code. the we combine our results and get the top 100 pages sorted by score.
    - *GET-* **serach_body** - in search_body_wiki (src/Searchbody.py) we first tokenize the query and then load all the relevant postings list according to the query using inverted_index_gcp_body.py. After that we load the pre-calculated data from the body index file into D and create tf-idf query vecotr Q. Those two are the input for cosine similarity function which retrives the distance between the query and each file in the relevant postings list. Those files are then sorted and cut to the top 100 results.
    For those results we retrieve the title using id2title.csv file.
    - *GET-* **serach_title** - in search_title_wiki (src/SearchTitle.py) we first tokenize the query and then load all the relevant postings list according to the query using binary_inverted_index_gcp_body.py. For all postings list returned we computed the score for each titled file how many common words appear both in the query and the posting title. Those are later sorted and retruned to the client.
    - *GET-* **serach_anchor** -- in search_anchor_wiki (src/SearchAnchor.py) we first tokenize the query and then load all the relevant postings list according to the query using binary_inverted_index_gcp_body.py. For all postings list returned we computed the score for each titled file how many common words appear both in the query and the posting anchor. Those are later sorted and retruned to the client.
    - *POST-* **get_pagerank** - retrieve_pagerank (src/Pagerank.py) function is initiated and for all title' id provided retrieves all of the ranks from pagerank file.
    - *POST-* **get_pageviews** -retrieve_pageviews (src/Pageview.py) function is initiated and for all title' id provided retrieves all of the ranks from pageviews file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
