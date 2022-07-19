
import json
import psycopg2
from fastapi import APIRouter,Request

import rdflib
router = APIRouter()
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import pdfx
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['queue']
sparql = SPARQLWrapper(
    "https://aida.kmi.open.ac.uk/sparqlendpoint"
)
def sparql_query():
    sparql.setReturnFormat(JSON)

    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint
    sparql.setQuery("""
PREFIX aida: <http://aida.kmi.open.ac.uk/ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX aidar: <http://aida.kmi.open.ac.uk/resource/>
SELECT *
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    aidar:2300368847 aida:hasTopic ?topic .
    ?topic owl:sameAs ?obj .
    FILTER(regex(str(?obj), "dbpedia" ) )
}
        """
    )

    try:
        ret = sparql.queryAndConvert()

        for r in ret["results"]["bindings"]:
            print(r)
    except Exception as e:
        print(e)

from routers.semantic_lookup import entity_lookup
from routers.papers_db import SessionLocal,engine
import routers.papers_models as models
@router.get("/api/papers/cso")
async def get_cso(arxiv_id: str):
    conn = psycopg2.connect("dbname=reader_app user=diego host=165.232.156.229 password=83o2Zw5GKzMQiH923u2OzKBHCZNUw")
    cur = conn.cursor()
    cur.execute("SELECT title,abstract,full_text,code,entity_links FROM papers WHERE arxiv_id = {}::text".format(str(arxiv_id)))
    try:
        rows = cur.fetchall()
        # print(rows)
        if len(rows) == 0:
            # Adding paper to priority queue
            collection.replace_one({
                "arxiv_id": arxiv_id,
                "base_processed": False,
            },{
                "arxiv_id": arxiv_id,
                "base_processed": False,
            },upsert=True)
            print("No rows returned from query")
            return
        else:
            rows = rows[0]
        conn.close()
        # print(rows[2])
        # print(rows[4])
        if rows[2] == None:
            pdf = pdfx.PDFx("https://arxiv.org/pdf/{}.pdf".format(arxiv_id))
            full_text = pdf.get_text()
        else:
            full_text = rows[2]
        if rows[4] == None or len(rows[4]) == 0:
            entities = entity_lookup(rows[0],rows[1],full_text)
            db = SessionLocal()
            db_paper = db.query(models.Paper).filter(models.Paper.arxiv_id == arxiv_id).first()
            entities = [json.dumps(e) for e in entities ]
            setattr(db_paper, 'entity_links', entities)
            db.commit()
            # Should probably update the DB too but its going to be added to the priority queue anyway so it's pretty much the same.
        else:
            entities = rows[4]
        
        return {
            "title": rows[0],
            "entities": entities
        }
    except Exception as e:
        print(e)
        if(rows[3]==None):
            code = None
        else:
            code = json.loads(rows[3])
        return {
            "code": code,
            "title": rows[0],
            "entities": []
        }
    # paper = {
    #     "title": rows[0],
    #     "abstract": rows[1]
    # }
    # result = cc.run(paper)




    # for s,p,o in g.triples((None,"http://schema.org/relatedLink",None)):
    #     print(s,p,o)

    for x in result["explanation"]:
        g = Graph()
        g.parse("https://cso.kmi.open.ac.uk/topics/{}.ttl".format(str(x).replace(" ","_")), format="turtle")
        # print(x)
    # print(result["explanation"]['computational linguistics'])
        for s,p,o in g:
            if(p.split("/")[-1]=="relatedLink"):
                # print("Found Related Link")
                if(str(o).startswith("http://en.wikipedia.org/wiki/")):
                    # print("Found Wikipedia Link")
                    url = str(o)
        for x in result["explanation"][x]:
            print("<a src='{}'>{}</a>".format(url,x))
    
    
    return result

            # print(s,p,o)
            # print(o)
    # for s, p, o, g in g.quads((None, RDF.type, None, None)):
    #     print(s, g)
    # for topic in result["topics"]:
    #     print(topic)
    # sparql_query()
    # return result
    # print(result.keys())
    # with open('cso.json', 'w') as f:
    #     f.write(json.dumps(result))
    # response = await get_bookmarks()
    # print(response)

    return {"message":"Hello World"}


@router.post("/api/papers/entity_link")
async def add_entity(request:Request):
    res = await request.json()
    print(res)
    arxiv_id = res['arxiv_id']
    link = res['link']
    db = SessionLocal()
    db_paper = db.query(models.Paper).filter(models.Paper.arxiv_id == arxiv_id).first()
    print(db_paper.entity_links)
    new_entities = db_paper.entity_links
    new_entities.append(link)
    print(new_entities)
    setattr(db_paper, 'entity_links', new_entities)
    db.commit()
    return {"message":"Added entity link to paper {}".format(arxiv_id)}
    
    return {"message":"Hello World"}
    



@router.get("/api/paper")
async def get_paper(arxiv_id: str):
    conn = psycopg2.connect("dbname=reader_app user=diego host=165.232.156.229 password=83o2Zw5GKzMQiH923u2OzKBHCZNUw")
    cur = conn.cursor()