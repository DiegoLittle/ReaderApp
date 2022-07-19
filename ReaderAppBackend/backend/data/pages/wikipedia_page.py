
from pydantic import BaseModel
from pymongo import MongoClient
import psycopg2
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
import wikipediaapi


client = MongoClient(conn_str)
db = client['research_papers']
collection = db['pages']
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')
wikipedia_pages = list(collection.find({"wikipedia_link":{"$exists":True}}
))
for wiki_page in wikipedia_pages:
    page_py = wiki_wiki.page(wiki_page['wikipedia_link'].split("wiki/")[-1])
    print(page_py.text)