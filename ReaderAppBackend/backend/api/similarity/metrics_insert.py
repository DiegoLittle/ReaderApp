import json
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
# tasks = list(collection.find({"type":"task"}))

# entities = list(collection.find({"sources": {"$in": [ 'paperswithcode']}}))

datasets = list(collection.find({"type":"dataset"}))

# For each dataset 
for dataset in datasets:
    if dataset.get('sota',None):
        metrics = dataset['sota'].get('metrics')
        # print(dataset['name'])
        for metric in metrics:
            metric_mongo = collection.find_one({"name":metric})
            if metric_mongo:
                collection.update_one({
                    "_id": metric_mongo['_id']
                },{'$push':{
                "evaluatesFor": dataset['name']
            }}
                )
            else:
                collection.insert_one({
                    "name": metric,
                    "type": "metric",
                    "evaluatesFor": [dataset['name']]
                })

#  