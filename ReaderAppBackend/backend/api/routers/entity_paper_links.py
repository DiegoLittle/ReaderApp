import sys
sys.path.append('../')
from database import SessionLocal, engine
import models
import json

from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']
# papers_entities = engine.execute("SELECT arxiv_id,code,entity_links FROM papers where arxiv_id is not null and entity_links is not null order by num_citations desc LIMIT 10000;").fetchall()
# papers = [{'arxiv_id': x[0],'code': x[1],'entity_links': x[2]} for x in papers_entities]




def set_code_array_and_entity_sources(worker):
    print("Worker: ", worker)
    db = SessionLocal()
    # db_paper = db.query(models.Entity).first()
    papers_query = db.query(models.Paper).filter(models.Paper.entity_links != None,models.Paper.arxiv_id != None).order_by(models.Paper.num_citations.desc()).offset(worker*200).limit(200).all()
    for paper in papers_query:
        # print(json.loads(paper.code)
        if paper.code:
            code = json.loads(paper.code)
            if(type(code) == dict):
                # db_paper = db.query(models.Paper).filter(models.Paper.arxiv_id == paper.arxiv_id).first()
                setattr(paper,"code",json.dumps([code]))
                db.commit()
                print("Updated code for paper: ",paper.arxiv_id)
        entity_links = [json.loads(entity) for entity in paper.entity_links]
        # Filter entity links with duplicate names
        filtered_entities = []
        entity_names = []
        for entity_link in entity_links:
            if entity_link['link']['name'] not in entity_names:
                entity_names.append(entity_link['link']['name'])
                filtered_entities.append(entity_link)
            else:
                print("Duplicate entity name: ", entity_link['link']['name'])


        
        for x in filtered_entities:
            source= {
                "arxiv_id": paper.arxiv_id,
                "type": "paper",
            }
            # Add the paper to the list of items that the entity appears in
            # sources.append(json.dumps(source))
            # entity json 
            db_entity = collection.find_one({
                "name": x['link']['name']
            })
            db_entity_ids = [x['arxiv_id'] for x in db_entity['appearsin']]
            if source['arxiv_id'] not in db_entity_ids:
                update_entity = collection.update_one(
                    {
                    'name': x['link']['name']},
                    {
                        '$push':{
                    "appearsin": source}
                    },upsert=True)
                print("Updated appearsin for entity: ",x['link']['name'])
            # setattr(db_entity,"appearsIn",sources)
            # db.commit()
            

    
    # print(paper.entity_links)

from multiprocessing import Process
import sys
def main(threads=1):
    print(threads)
    processes = []
    for i in range(threads):
        p = Process(target=set_code_array_and_entity_sources, args=(i,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


if __name__ == '__main__':
    print("Starting...")
    try:
        threads = int(sys.argv[1])
    except IndexError:
        threads = 0
    main(threads)