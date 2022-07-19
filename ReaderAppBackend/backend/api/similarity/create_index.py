import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from annoy import AnnoyIndex
import sys
sys.path.append('../')
from database import SessionLocal, engine
import json
import numpy as np
# print("Building spans search index for semantic search")
# f = open('all_entities.json')
# data = json.load(f)

# # Get array of all labels
# labels = []
# for i in data:
#     label = i.get('name')
#     labels.append(label)





# print(len(labels))
import json
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
import re
# regx = re.compile("/resource/", re.IGNORECASE)
terms = list(collection.find({}))

terms = [term for term in terms if term.get('type',None) != 'resource']
ml_terms = []
for term in terms:
    term['_id'] = str(term['_id'])
    ml_terms.append(term)


# labels = [term['name'] for term in ml_terms]

with open("ml_terms.json", "w") as f:
    f.write(json.dumps(ml_terms))

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

    # with open('papers.json', 'w') as f:
    #     json.dump([dict(x) for x in papers], f)


    # index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    # index.add_with_ids(encoded_data, np.array(range(0, len(data))))

    # faiss.write_index(index, name)

# create_index('ml_terms',labels)