import json
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
tasks = list(collection.find({"type":"task"}))
datasets_db = list(collection.find({"type":"dataset"}))


with open("evaluation-tables.json", "r") as f:
    data = json.load(f)
    print(len(data))

# with open("test.json", "w") as f:
#     json.dump(data[0], f)

task_names = [task['name'] for task in tasks]
dataset_names = [dataset['name'] for dataset in datasets_db]
not_found = 0
found = 0
found_dataset = 0
not_found_dataset = 0
for i in data:
    if i['task'] not in task_names:
        not_found += 1
        task = {}
        task["name"] =i['task']
        if i['description'] != "":
            task["task_description"] = i['description']
        if len(i['categories']) > 0:
            task['tags'] = i['categories']
        if i['source_link']:
            task['url'] = i['source_link']
        if len(i['subtasks']) > 0:
            task['subtasks'] = i['subtasks']
        if len(i['datasets']):
            task['datasets'] = i['datasets']
        # print("Task not found: " + i['task'])
        task['sources'] = ["paperswithcode"]
        task['type'] = "task"
        collection.insert_one(task)
        task_names.append(task['name'])

    else:
        # Find task in mongo and add dataset to it
        task = collection.find_one({
            "name": i['task']
        })

        if i['description'] != "" and task.get('description',None) == None:
            task['description'] = i['description']
        if len(i['categories']) > 0:
            task['tags'] = i['categories']
        # print(i.keys())
        if i['source_link']:
            task['source_link'] = i['source_link']
        if len(i['subtasks']) > 0:
            task['subtasks'] = i['subtasks']
        if len(i['datasets']):
            task['datasets'] = i['datasets']
        print(task['_id'])
        collection.replace_one({
            "_id": task['_id']
        },task)


        # print("Task found: " + i['task'])
        found += 1
    for dataset in i['datasets']:
        dataset_name = dataset['dataset']
        if dataset_name not in dataset_names:
            # Finding Adding dataset to mongo
            not_found_dataset += 1
            db_dataset = {}
            db_dataset['task'] = i['task']
            db_dataset['name'] = dataset_name
            if dataset['description'] != "":
                db_dataset['description'] = dataset['description']
            if len(dataset['subdatasets']) > 0:
                db_dataset['subdatasets'] = dataset['subdatasets']
            if len(dataset['dataset_links']) > 0:
                db_dataset['dataset_links'] = dataset['dataset_links']
            db_dataset['sota'] = dataset['sota']
            if (len(dataset['dataset_citations'])) > 0:
                db_dataset['citations'] = dataset['dataset_citations']
            task['sources'] = ["paperswithcode"]
            task['type'] = "dataset"
            collection.insert_one(db_dataset)
            dataset_names.append(dataset_name)
            
            # print("Dataset not found: " + dataset_name)
        else:
            # Finding existing dataset and adding new values and task name
            db_dataset = collection.find_one({
                "name": dataset_name
            })
            db_dataset['task'] = i['task']
            db_dataset['name'] = dataset_name
            if dataset['description'] != "" and db_dataset.get('description',None) == None:
                db_dataset['description'] = dataset['description']
            if len(dataset['subdatasets']) > 0:
                db_dataset['subdatasets'] = dataset['subdatasets']
            if len(dataset['dataset_links']) > 0:
                db_dataset['dataset_links'] = dataset['dataset_links']
            db_dataset['sota'] = dataset['sota']
            if (len(dataset['dataset_citations'])) > 0:
                db_dataset['citations'] = dataset['dataset_citations']
            print(db_dataset['_id'])
            collection.replace_one({
                "_id": db_dataset['_id']
            },db_dataset)
            # collection.insert_one(db_dataset)
            found_dataset += 1
            # print("Dataset found: " + dataset_name)


with open("datasets.json","r") as f:
    datasets = json.load(f)
    print(len(datasets))

# If task is not found, add it to the tasks
# Add the datast
# If dataset is not found, add it to the datasets
# All tasks should be linked with datasets
# all datasets should be linked with tasks

print("Not found: " + str(not_found))
print("Found: " + str(found))
print("Not found dataset: " + str(not_found_dataset))
print("Found dataset: " + str(found_dataset))


