import numpy as np
import torch
import os
import pandas as pd
import time
from sentence_transformers import SentenceTransformer
import json
from pymongo import MongoClient
import torch
torch.set_num_threads(1)
f = open('resources_spaced.json')
data = json.load(f)
# Get array of all labels

print("Loading model")
model = SentenceTransformer('all-MiniLM-L6-v2')

from annoy import AnnoyIndex
def search_spans(query,k=10):

    query_vec = model.encode(query,device='cpu',convert_to_numpy=True)
    f=384
    u = AnnoyIndex(f, 'angular')
    u.load('resources_index.ann') # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [data[x] for x in search[0]]
    scores = search[1]
    # if(results[0]['arxiv_id'] == arxiv_id):
    #     results.pop(0)
    return {
        "labels": labels,
        "scores": scores
    }

res = search_spans("rdf")
print(res)
# if __name__ == "__main__":
#     # create_index('spans_index',labels)
#     # search("Test")