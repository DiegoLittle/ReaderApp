import json
from sentence_transformers import SentenceTransformer,util
import torch
import time
import numpy as np
with open("ml_terms.json", "r") as read_file:
    ml_terms = json.load(read_file)

model = SentenceTransformer('all-MiniLM-L6-v2')


start = time.time()
ml_terms_vec = model.encode(ml_terms[:50])
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


with open("all_entities.json", "r") as f:
    all_terms = json.loads(f.read())


cosine_similarities = []
for term in all_terms:
    # print(term['name'])
    term_vec = model.encode(term['name'])
    cosine_scores = util.cos_sim(sum_vec, term_vec)
    term_cosine ={
        "name":term['name'],
        "cosine_score":cosine_scores
    }
    cosine_similarities.append(term_cosine)

with open("cosine_similarities.json", "w") as f:
    f.write(json.dumps(cosine_similarities))


