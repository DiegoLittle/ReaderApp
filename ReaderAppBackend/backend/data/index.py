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
# print("Building spans search index for semantic search")
f = open('resources_spaced.json')
data = json.load(f)

# data = [x.replace("_"," ") for x in data]

# # Get array of all labels
# labels = []
# for i in data:
#     label = i.get('name')
#     labels.append(label)



# import models,schemas
# def create_spans_from_DB():

#     res = [{
#         "id":x.id,
#         "name":x.name,
#         "full_name":x.full_name,
#         "url":x.url,
#     } for x in engine.execute("SELECT id,name,full_name,url FROM entities;").fetchall()]

#     with open("db_entities.json", "w") as f:
#         json.dump(res, f)


def create_index(name,data:list):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoded_data = model.encode(data)
    print("Building faiss index")
    print(encoded_data.shape)



    f = 384  # Length of item vector that will be indexed
    i=0
    t = AnnoyIndex(f, 'angular')
    for i in range(len(encoded_data)):
        v = encoded_data[i]
        # print(v)
        t.add_item(i, v.tolist())

    t.build(10) # 10 trees
    t.save('resources_index.ann')



    # with open('papers.json', 'w') as f:
    #     json.dump([dict(x) for x in papers], f)


    # index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    # index.add_with_ids(encoded_data, np.array(range(0, len(data))))

    # faiss.write_index(index, name)

create_index('spans_index',data)