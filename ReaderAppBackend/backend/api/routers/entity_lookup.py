from sqlalchemy.orm import Session
import os
import hashlib
import base64
from datetime import datetime, timedelta, tzinfo
from typing import Optional, OrderedDict
import json
import sys
sys.path.append('../')
from routers.semantic_lookup import entity_lookup
from papers_db import SessionLocal,engine
import datetime
# res = engine.execute("SELECT title,abstract,full_text,arxiv_id,date FROM papers where entity_links is null and arxiv_id is not null order by date DESC limit 100;").fetchall()
from dateutil import parser
import datetime
import time

from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler



def get_sorted_papers():
    today = datetime.datetime.today().replace(tzinfo=None)
    stats = engine.execute("SELECT num_citations,date,arxiv_id FROM papers where arxiv_id is not null").fetchall()
    all_citations = [x[0] for x in stats]
    #set none to 0
    all_citations = [x if x is not None else 0 for x in all_citations]

    all_dates = [x[1] for x in stats]
    # Convert dates to days old
    all_dates = [parser.parse(x).replace(tzinfo=None) for x in all_dates]
    num_days_old = [(today-x).days for x in all_dates]

    x_array = np.array(num_days_old)
    normalized_dates = preprocessing.normalize([x_array])[0]
    citations_np = np.array(all_citations)
    normalized_citations = preprocessing.normalize([citations_np])[0]
    # from sklearn.preprocessing import MinMaxScaler
    # scaler = MinMaxScaler()
    # Plot the data using matplotlib
    # plt.plot(normalized_dates, normalized_citations, 'ro')
    # plt.xlabel('Days Old')
    # plt.ylabel('Citations')
    # plt.savefig('test.png')
    results = []
    for x in range(len(normalized_citations)):
        print(normalized_dates[x],normalized_citations[x])
        citation_weight = 1
        date_weight = -1
        # Date might not be properly weighted because less is more
        score = (normalized_dates[x]*date_weight) + (citation_weight *normalized_citations[x])
        results.append({
            "num_citations":stats[x][0],
            "date":stats[x][1],
            "score":score,
            "arxiv_id":stats[x][2]
        })
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    # print(results[5:])
    with open("citations_sorted.json", "w") as f:
        json.dump(results, f,indent=4)




with open("citations_sorted.json","r") as f:
    res = json.loads(f.read())

import routers.papers_models as models



for paper in res:
    arxiv_id = paper['arxiv_id']
    db = SessionLocal()
    db_paper = db.query(models.Paper).filter(models.Paper.arxiv_id == arxiv_id).first()
    if db_paper.entity_links is not None:
        print("Already computed entity links for {}".format(arxiv_id))
        continue
    if db_paper.full_text == "" or db_paper.full_text == None:
        print("No full text found for paper: {}".format(arxiv_id))
        continue
    entities = entity_lookup(db_paper.title,db_paper.abstract,db_paper.full_text)
    entities = [json.dumps(e) for e in entities ]
    # setattr(db_paper, 'entity_links', entities)
    # db.commit()
    print("Adding entity links to paper: {}".format(arxiv_id))
    print("Adding paper to entity links")
    
    for entity in entities:
        print(entity['name'])
    




