import json
import sys
sys.path.append('../')
import models,schemas
from database import engine
import json
import pandas as pd
import requests
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
tasks = list(collection.find({{"type":"task"}}))

# all_entities = []



def create_spans_from_DB():
    res = [{
        "id":x.id,
        "name":x.name,
        "description":x.description,
        "type":x.entity_type,
        "full_name":x.full_name,
        "url":x.url,
        "sources": ["paperswithcode"]
    } for x in engine.execute("SELECT id,name,description,full_name,url,entity_type,synonyms FROM entities;").fetchall()]

    return res
    # with open("db_entities_.json", "w") as f:
    #     json.dump(res, f)





def get_cskg_spans():
    with open('files/cskg_spans.json','r') as f:
        cskg_spans = json.load(f)
    return cskg_spans

def write_spans(db_entities,cskg_spans):
    cskg_spans.extend(db_entities)
    with open('all_entities.json','w') as f:
        json.dump(cskg_spans,f)


def read_all_entities():
    with open('all_entities.json','r') as f:
        all_entities = json.load(f)
    return all_entities

def fetch_mongo_entities():
    mongo_methods = list(collection.find({}))
    return mongo_methods

# db_entities = create_spans_from_DB()

# cskg_spans = get_cskg_spans()
# write_spans(db_entities,cskg_spans)
# all_entities = fetch_mongo_entities()
# print(len(all_entities))
# all_entities = read_all_entities()
# collection.insert_many(all_entities)

db_spans = create_spans_from_DB()

with open('files/google_ml-glossary.json','r') as f:
    google_terms = json.load(f)

all_spans = db_spans.extend(google_terms)



# collection.update_many({
#     "source":"cskg"
# },{'$unset':{'source':"cskg"}})
def entity_lookup_and_insert():

    for term in google_terms:
        res = requests.get("http://localhost:8000/api/search?q=" + term['name'])
        data = res.json()
        if data['scores'][0] == 0:
            # print(term['name'])
            continue
            # print(data['labels'][0])
            # print(term)

        elif data['scores'][0] < .05 and data['scores'][0] > 0:
            continue
            # print(term['name'])
            # print(data['labels'][0])
            # print(data['scores'][0])
            pass
            # collection.update_one(
            # {
            #     'name':term['name']},
            #     {
            #     '$set':{
            #     'description':term['definition'],
            #     },
            #     '$push':{
            #         "sources": "google_ml"
            #     },
            #     },
            #     upsert=False
            #     )
            
        else:
            collection.insert_one({
                "name": term['name'],
                "description": term['definition'],
                "sources": ['google_ml']
            })


# with open('db_entities.json','r') as f:
#     db_entities = json.load(f)


# all_entities = fetch_mongo_entities()
# print(len(all_entities))

# For item that contains cskg in source
# query cskg 


