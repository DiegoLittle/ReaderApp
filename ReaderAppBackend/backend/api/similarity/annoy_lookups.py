import numpy as np
import torch
import os
import pandas as pd
import time
from sentence_transformers import SentenceTransformer
import json
from pymongo import MongoClient
import torch
import sys
sys.path.append('../')
torch.set_num_threads(1)
try:
    f = open('/Users/diego/Documents/Projects/ReaderAppBackend/backend/api/similarity/all_entities.json')
    data = json.load(f)
except FileNotFoundError:
    f = open('all_entities.json')
    data = json.load(f)

# # Get array of all labels
# labels = []
# for i in data:
#     label = i.get('label')
#     labels.append(label)

# f = open("similarity/all_entities.json")

print("Loading model")
model = SentenceTransformer('all-MiniLM-L6-v2')

from annoy import AnnoyIndex
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
def search_spans(query,k=10):

    query_vec = model.encode(query,device='cpu',convert_to_numpy=True)
    f=384
    u = AnnoyIndex(f, 'angular')
    u.load('/Users/diego/Documents/Projects/ReaderAppBackend/backend/api/similarity/all_entities_index.ann') # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [data[x]for x in search[0]]
    scores = search[1]
    # if(results[0]['arxiv_id'] == arxiv_id):
    #     results.pop(0)
    
    results_list =  {
        "labels": labels,
        "scores": scores
    }
    try:
        if abs(results_list['scores'][0] - results_list['scores'][1]) <= 0.1:
            if (results_list['labels'][0].get('type') is not None) and (results_list['labels'][1].get('type') is None):
                results_list['labels'][0], results_list['labels'][1] = results_list['labels'][1], results_list['labels'][0]
            # if results_list['labels'][0].get('type',None) == 'cskg' and results_list['labels'][1].get('type',None) == None:
                
    except Exception as e:
        print(e)
        pass
    return results_list

with open("/Users/diego/Documents/Projects/ReaderAppBackend/backend/api/similarity/ml_terms.json", "r") as read_file:
    ml_terms = json.load(read_file)

def search_terms(query,k=10):

    query_vec = model.encode(query,device='cpu',convert_to_numpy=True)
    f=384
    u = AnnoyIndex(f, 'angular')
    u.load('similarity/ml_terms.ann') # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [ml_terms[x]for x in search[0]]
    scores = search[1]
    # if(results[0]['arxiv_id'] == arxiv_id):
    #     results.pop(0)
    
    results_list =  {
        "labels": labels,
        "scores": scores
    }
    try:
        if abs(results_list['scores'][0] - results_list['scores'][1]) <= 0.1:
            if (results_list['labels'][0].get('type') is not None) and (results_list['labels'][1].get('type') is None):
                results_list['labels'][0], results_list['labels'][1] = results_list['labels'][1], results_list['labels'][0]
            # if results_list['labels'][0].get('type',None) == 'cskg' and results_list['labels'][1].get('type',None) == None:
                
    except Exception as e:
        print(e)
        pass
    return results_list



# if __name__ == "__main__":
#     # create_index('spans_index',labels)
#     # search_spans("Test")
#     # res = search_terms("Test")
#     # print(res)
