from pydantic import BaseModel
from pymongo import MongoClient
import psycopg2
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"


client = MongoClient(conn_str)
db = client['research_papers']
collection = db['pages']


# pages_without_desc = str(len(list(collection.find({'description': {'$exists': False}}))))
# print("Total page: " + str(len(list(collection.find()))))
# print("Total pages without description: " + str(len()))
# print("Percent of pages without description: " + /collection.find().count()))

no_descriptions = list(collection.find({'description': {'$exists': False}}))

print(no_descriptions[0])