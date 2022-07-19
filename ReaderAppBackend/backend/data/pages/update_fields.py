from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import json
from pymongo import MongoClient
import psycopg2
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
from psycopg2.extras import RealDictCursor

# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
# "postgresql://diego:83o2Zw5GKzMQiH923u2OzKBHCZNUw@165.232.156.229:5432/reader_app"

class Page(BaseModel):
    title: str
    slug: str
    resource_name: str
    aliases: list[str]
    description: str
    related_papers: list
    datasets: list
    related_concepts: list
    tags: list
    type: str


# class Dataset(BaseModel):
#     name = str
#     description = str
#     introduced_date = str
#     modalities = str
#     tasks = str
#     languages = str
#     variants = str
#     num_papers = str
#     data_loaders = Column(ARRAY(String))
# mongo_datasets = list(collection.find({
#     'type': 'dataset'
# }))

with open("datasets_fix.json") as f:
    datasets = json.load(f)
    # Add missing fields to mongo_datasets

for dataset in datasets:
    mongo = collection.find_one({
        "name": dataset['name']
    })
    if mongo is None:
        print("Adding new dataset: " + dataset['name'])
        collection.insert_one(dataset)
        continue
    updated_fields_count = 0
    for key in dataset.keys():
        if key not in mongo:
            mongo[key] = dataset[key]
            updated_fields_count += 1
    print("Updated {} fields for dataset: {}".format(updated_fields_count, dataset['name']))
    if (updated_fields_count > 0):
        update_res = collection.replace_one({
            "name": dataset['name'],
        },
        mongo
        )


def update_new_fields(new_list, collection):
    for item in new_list:
        mongo = collection.find_one({
            "name": item['name']
        })
        if mongo is None:
            print("Adding new item: " + item['name'])
            collection.insert_one(item)
            continue
        updated_fields_count = 0
        for key in item.keys():
            if key not in mongo:
                mongo[key] = item[key]
                updated_fields_count += 1
        print("Updated {} fields for item: {}".format(updated_fields_count, item['name']))
        if (updated_fields_count > 0):
            update_res = collection.replace_one({
                "name": item['name'],
            },
            mongo
            )


with open('methods_fix.json') as f:
    methods = json.load(f)
update_new_fields(methods,collection)

    # Add missing fields to mongo_methods
    # print("Updated: ", mongo['name'])



# def create_page(entity):

    # page_id = collection.insert_one(page.__dict__).inserted_id
    # return page_id