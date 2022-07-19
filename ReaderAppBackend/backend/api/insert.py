from sqlalchemy.orm import Session
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional, OrderedDict
import json
from psycopg2.errors import UniqueViolation
import psycopg2
import models,schemas
from database import SessionLocal,engine
from sqlalchemy.exc import IntegrityError
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['methods']

mongo_methods = list(collection.find({}))

data = mongo_methods

# with open('../downloads/datasets.json') as f:
#     data = json.load(f)
# with open('../downloads/methods.json') as f:
#     data = json.load(f)

def map_to_db_tasks(data):
    db_item = models.Task(
        name=data['task'],
        url=data['url'],
        datasets=data['datasets'],
    )
    return db_item
db_tasks = engine.execute("SELECT id,name FROM entities;").fetchall()
names = [x.name for x in db_tasks]
# print([x] for x in db_tasks)
# print(db_tasks)

def map_to_db_datasets(data):
    task_ids = []
    for x in data['tasks']:
        # print(x['task'])
        task_ids.append(db_tasks[names.index(x['task'])][0])
        # db_task = engine.execute("SELECT id FROM entities WHERE name = '{}'".format(x['task']))
        # task_id = db_task.fetchone()[0]
        # task_ids.append(task_id)
    db_item = models.Dataset(
        name=data['name'],
        url=data['url'],
        description=data['description'],
        full_name=data['full_name'],
        homepage=data['homepage'],
        paper=json.dumps(data['paper']),
        introduced_date=data['introduced_date'],
        modalities=data['modalities'],
        tasks=task_ids,
        languages=data['languages'],
        variants=data['variants'],
        num_papers=data['num_papers'],
        data_loaders=json.dumps(data['data_loaders']),
    )
    return db_item
        
def map_to_db_methods(data):
    # print(data.keys())
    db_item = models.Method(
        name=data['name'],
        url=data['url'],
        description=data['description'],
        full_name=data['full_name'],
        paper=json.dumps(data['paper']),
        introduced_date=data.get('introduced_date',None),
        source_url = data['source_url'],
        source_title = data['source_title'],
        code_snippet_url = data['code_snippet_url'],
        num_papers = data['num_papers'],
        collections = [json.dumps(x) for x in data['collections']],
        papers_mentioned = data['papers_mentioned']
    )
    return db_item

def insert_tasks(data):
    tasks = []
    for item in data:
        # For each task in the dataset
        for task in item['tasks']:
            # 
            task['datasets'] = [item['url']]
            task_names = [x['task'] for x in tasks]
            if task['task'] in task_names:
                # print(tasks[task_names.index(task['task'])])
                tasks[task_names.index(task['task'])]['datasets'].append(item['url'])
                # print(tasks[task_names.index(task['task'])]['datasets'])
                # print(f'Task {task["task"]} already exists')
            else:
                tasks.append(task)
    
    db_tasks = list(map(map_to_db_tasks,tasks))
    db = SessionLocal()
    db.bulk_save_objects(db_tasks)
    db.commit()

def insert_databases(data):

    datasets = []
    for item in data:
        if(item['name'] in names):
            # Remove from data
            data.remove(item)
            
    datasets = list(map(map_to_db_datasets,data))
    db = SessionLocal()
    db.bulk_save_objects(datasets)
    db.commit()

def insert_methods(data):
    methods = []
    for item in data:
        if(item['name'] in names):
            # Remove from data
            data.remove(item)
    methods = list(map(map_to_db_methods,data))
    db = SessionLocal()
    db.bulk_save_objects(methods)
    db.commit()
insert_methods(data)

# insert_databases(data)

# result = engine.execute("SELECT * FROM entities WHERE entity_type = 'task';")
# db_tasks = result.fetchall()
# task_names = [task['name'] for task in db_tasks]
# for task in [x for x in tasks if x is not None]:
#     if task['task'] not in task_names:
#         db_tasks = list(map(map_to_db_tasks,tasks))
        # try:

        #     db = SessionLocal()
        #     db_item = models.Task(
        #     name=task['task'],
        #     url=task['url']
        # )
        #     db.add(db_item)
        #     db.commit()
        #     task_names.append(task['task'])
        #     print("Adding task: {}".format(task['task']))
        # except IntegrityError as e:
        #     if(type(e.orig) == UniqueViolation):
        #         print("Task already exists: {}".format(task['task']))
            
        #         db.rollback()
        #         print("Rolling back")
        #         continue
        #     else:
        #         raise e


    # except Exception as e:
    #     print(e)



# db = SessionLocal()

# db_item = models.Dataset(
#     name="COCO",
#     description="test", 
#     homepage="https://cocodataset.org",   
# )
# db.add(db_item)
# db.commit()
# db_item = models.Method(
#     name="COCO",
#     description="test", 
# )
# db.add(db_item)
# db.commit()
# db.refresh(db_item)
# return db_item



