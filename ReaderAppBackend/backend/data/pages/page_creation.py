from pydantic import BaseModel
from pymongo import MongoClient
import psycopg2
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"


client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']



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


def create_dataset_pages():
    mongo_datasets = list(collection.find({
    'type': 'dataset'
    }))
    for dataset in mongo_datasets:
        del(dataset['_id'])

        slug = dataset['name'].replace(' ', '_')
        dataset['title'] = dataset['name']
        del(dataset['name'])
        dataset['slug'] = slug
        dataset['resource_name'] = dataset['slug']
        

        paper = dataset.get('paper',None)
        if paper:
            dataset['related_papers'] = [paper]
        db['pages'].replace_one({
            "title": dataset['title']
        },dataset,upsert=True)
        print("Created : " + dataset['title'])

def create_methods_pages():
    mongo_methods = list(collection.find({
    'type': 'method'
    }))
    for method in mongo_methods:
        del(method['_id'])

        slug = method['name'].replace(' ', '_')
        method['title'] = method['name']
        del(method['name'])
        method['slug'] = slug
        method['resource_name'] = method['slug']
        

        paper = method.get('paper',None)
        if paper:
            method['related_papers'] = [paper]
        db['pages'].replace_one({
            "title": method['title']
        },method,upsert=True)
        print("Created : " + method['title'])

def create_task_pages():
    mongo_tasks = list(collection.find({
    'type': 'task'
    }))
    for task in mongo_tasks:
        del(task['_id'])
        slug = task['name'].replace(' ', '_')
        task['title'] = task['name']
        del(task['name'])
        task['slug'] = slug
        task['resource_name'] = task['slug']
        paper = task.get('paper',None)
        if paper:
            task['related_papers'] = [paper]
        db['pages'].replace_one({
            "title": task['title']
        },task,upsert=True)
        print("Created : " + task['title'])

def create_ml_terms():
    mongo_ml_terms = list(collection.find({"sources":{"$in":["google_ml"]}}))
    for ml_term in mongo_ml_terms:
        del(ml_term['_id'])
        slug = ml_term['name'].replace(' ', '_')
        ml_term['title'] = ml_term['name']
        del(ml_term['name'])
        ml_term['slug'] = slug
        ml_term['resource_name'] = ml_term['slug']
        paper = ml_term.get('paper',None)
        if paper:
            ml_term['related_papers'] = [paper]
        db['pages'].replace_one({
            "title": ml_term['title']
        },ml_term,upsert=True)
        print("Created : " + ml_term['title'])

# create_task_pages()
# create_ml_terms()
def capitalize_titles():
    all_pages = db['pages'].find({})
    for page in all_pages:
        if len(page['title'].split(" ")) > 1:
            if page['title'] != page['title'].title():
                db['pages'].update_one({
                    'title': page['title'],
                },{
                    '$set':{
                        'title': page['title'].title()
                    }
                }
                )

        