import json
from sentence_transformers import SentenceTransformer,util
import torch
import time
import numpy as np
import pickle
model = SentenceTransformer('all-MiniLM-L6-v2')

from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
entities = db['entities']



def get_average_vec():
    with open("ml_terms.json", "r") as read_file:
        ml_terms = json.load(read_file)

    model = SentenceTransformer('all-MiniLM-L6-v2')


    start = time.time()
    ml_terms_vec = model.encode(ml_terms)
    end = time.time()
    print(type(ml_terms_vec))
    print("Time taken to encode: ", end - start)
    f=384
    print(ml_terms_vec.shape)
    # print(ml_terms_vec.mean())

    sum_vec = torch.zeros(f)
    for vec in  ml_terms_vec:
        sum_vec += vec
    print(sum_vec/len(ml_terms_vec))

    # Store data (serialize)
    with open('average_vec.pickle', 'wb') as handle:
        pickle.dump(sum_vec, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Load data (deserialize)
with open('average_vec.pickle', 'rb') as handle:
    average_vec = pickle.load(handle)
    print(average_vec)
with open("all_entities.json", "r") as f:
    all_terms = json.loads(f.read())

import time
# cosine_similarities = []
# for index,term in enumerate(all_terms):
#     # print(term['name'])
#     term_vec = model.encode(term['name'])
#     cosine_scores = util.cos_sim(average_vec, term_vec)
#     term_cosine ={
#         "name":term['name'],
#         "cosine_score":cosine_scores.tolist()
#     }
#     cosine_similarities.append(term_cosine)
#     print(index)
#     if index % 500 == 0:
#         with open("cosine_similarities.json", "w") as f:
#             f.write(json.dumps(cosine_similarities))
#             # Store data (serialize)
#         with open('cosine_similarites.pickle', 'wb') as handle:
#             pickle.dump(cosine_similarities, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open("/Users/diego/Documents/Projects/ReaderAppBackend/backend/api/similarity/cosine_similarities.json","r") as f:
    data = json.loads(f.read())

cskgs = entities.find({
    'type': 'resource'
})
# if cskg
cskgs_terms = [x['name'] for x in cskgs]
# Get items in data that are cskg resources
cskg_cosines = [i for i in data if i['name'] in cskgs_terms]



values = [i['cosine_score'][0][0] for i in cskg_cosines]
# Standard deviation of list
# Using sum() + list comprehension
mean = sum(values) / len(values)
variance = sum([((x - mean) ** 2) for x in values]) / len(values)
res = variance ** 0.5

# Printing result
print("Standard deviation of sample is : " + str(res))
print("Average cosine score : {}".format(mean))

one_deviation = 0
two_deviation = []
three_deviation = 0
for i in cskg_cosines:
    if i['cosine_score'][0][0] > mean + res or i['cosine_score'][0][0] < mean - res:
        two_deviation.append(i)
        # print(i['name'])
    elif i['cosine_score'][0][0] > mean + res*2 or i['cosine_score'][0][0] < mean - res*2:
        three_deviation += 1
        # print(i['name'])
    else:
        one_deviation += 1
    
print("One deviation : {}".format(one_deviation))
print("Two deviation : {}".format(two_deviation))
print("Three deviation : {}".format(three_deviation))
print(len(two_deviation))


# The deviations change when the items are deleted so running it again could delete good ones

delete_count = 0
for x in two_deviation:
    # print(x)
    print(delete_count)
    delete_result = db['entities'].delete_one({'name':x['name'] })
    print(delete_result.deleted_count)
    delete_count += 1
    # print("Deleted: {}".format(x['name']))
    
