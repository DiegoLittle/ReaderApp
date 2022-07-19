import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from annoy import AnnoyIndex
import sys
sys.path.append('../')
# from database import SessionLocal, engine
import json
import numpy as np




# print(len(labels))
import json
from pymongo import MongoClient
import time
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['pages']

# regx = re.compile("/resource/", re.IGNORECASE)

start = time.time()
pages = list(collection.find({}))
for page in pages:
    page['_id'] = str(page['_id'])
end = time.time()
print(end-start)
with open("wiki_pages.json","w") as f:
    json.dump(pages,f)


# labels = [term['name'] for term in ml_terms]

def create_index(name,data:list):

    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    encoded_data = model.encode(data)
    print("Building annoy index")
    print(encoded_data.shape)



    f = 768  # Length of item vector that will be indexed
    i=0
    t = AnnoyIndex(f, 'angular')
    for i in range(len(encoded_data)):
        v = encoded_data[i]
        # print(v)
        t.add_item(i, v.tolist())

    t.build(10) # 10 trees
    t.save(name+'.ann')

titles = [page['title'] for page in pages]

# create_index("wiki_pages",titles)


def add_to_index(name,data:list):
    f = 768  # Length of item vector that will be indexed
    u = AnnoyIndex(f, 'angular')
    u.load(name+'.ann')

    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    encoded_data = model.encode(data)

    # u.add_item()


def search_spans(query,k=10):
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    query_vec = model.encode(query,device='cpu',convert_to_numpy=True)
    f=768
    u = AnnoyIndex(f, 'angular')
    u.load('wiki_pages.ann') # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [pages[x]for x in search[0]]
    scores = search[1]
    # if(results[0]['arxiv_id'] == arxiv_id):
    #     results.pop(0)
    
    results_list =  {
        "labels": labels,
        "scores": scores
    }
    # try:
    #     if abs(results_list['scores'][0] - results_list['scores'][1]) <= 0.1:
    #         if (results_list['labels'][0].get('type') is not None) and (results_list['labels'][1].get('type') is None):
    #             results_list['labels'][0], results_list['labels'][1] = results_list['labels'][1], results_list['labels'][0]
    #         # if results_list['labels'][0].get('type',None) == 'cskg' and results_list['labels'][1].get('type',None) == None:
                
    # except Exception as e:
    #     print(e)
    #     pass
    return results_list


if __name__ == "__main__":
    # print(create_index("wiki_pages",titles))
    # print(search_spans("deep learning"))
    print("")
