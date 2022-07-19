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
import time
# regx = re.compile("/resource/", re.IGNORECASE)

print("Loading resources")
start = time.time()
with open("/Users/diego/Documents/Projects/ReaderAppBackend/backend/data/kg/aikg_resources.json","r") as f:
    resources = json.load(f)
end = time.time()
print("Loaded resources in " + str(end-start) + " seconds")

# names = [resource['name'] for resource in resources]

# labels = [term['name'] for term in ml_terms]

def create_index(name,data:list):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoded_data = model.encode(data)
    print("Building annoy index")
    print(encoded_data.shape)



    f = 384  # Length of item vector that will be indexed
    i=0
    t = AnnoyIndex(f, 'angular')
    for i in range(len(encoded_data)):
        v = encoded_data[i]
        # print(v)
        t.add_item(i, v.tolist())

    t.build(10) # 10 trees
    t.save(name+'.ann')


# create_index("wiki_pages",names)


def add_to_index(name,data:list):
    f = 768  # Length of item vector that will be indexed
    u = AnnoyIndex(f, 'angular')
    u.load(name+'.ann')

    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    encoded_data = model.encode(data)

    # u.add_item()


def search_spans(query,k=10):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = model.encode(query,device='cpu',convert_to_numpy=True)
    f=384
    u = AnnoyIndex(f, 'angular')
    u.load('cskg_resources.ann') # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [resources[x]for x in search[0]]
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
    # print(create_index("cskg_resources",names))
    print(search_spans("Tuning"))
