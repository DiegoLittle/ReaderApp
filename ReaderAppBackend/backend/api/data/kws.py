from datetime import datetime, timedelta
from typing import Optional, OrderedDict
import json
import sys
sys.path.append('../')

import models,schemas
from database import SessionLocal,engine
from cso_classifier import CSOClassifier
cc = CSOClassifier(modules = "both", enhancement = "first", explanation = True)

db = SessionLocal()
papers = db.query(models.Paper).filter(models.Paper.keywords != None).order_by(models.Paper.date.desc()).limit(1000).all()
with open("keywords_updated.json","r") as f:
    data = json.loads(f.read())
papers = [paper for paper in papers if paper.arxiv_id not in data]

arxiv_ids = [p.arxiv_id for p in papers]

for paper in papers:
    paper_doc = {
        "title": paper.title,
        "abstract": paper.abstract
    }
    result = cc.run(paper_doc)
    # print(paper.title)
    # print(paper.keywords)
    print(paper.keywords)
    yake_keywords = [x[0] for x in json.loads(paper.keywords)]
    yake_scores = [x[1] for x in json.loads(paper.keywords)]
    cso_keywords = result['enhanced']
    all_keywords = []
    all_keywords.extend(yake_keywords)
    all_keywords.extend(cso_keywords)
    keywords_attr =     {
        "all": all_keywords,
        "yake": {
            "keywords": yake_keywords,
            "scores": yake_scores
        },
        "cso": {
            "keywords": cso_keywords,
        }
    }
    # setattr(paper, 'keywords', json.dumps(keywords_attr))
    # db.commit()
    print("Updated keywords for {}".format(paper.title))

print(arxiv_ids)

for id in arxiv_ids:
    data.append(id)
with open("keywords_updated.json", "w") as f:
    f.write(json.dumps(data))
# keywords = {
#     "yake": {
#         "keywords" ["test"],
#         "scores" [0.5]
#     },
#     "cso": {
#         "keywords" ["test"]        
# }