from fastapi import APIRouter
from database import SessionLocal,engine
router = APIRouter()
import json
# client = Minio("s3.amazonaws.com", "ACCESS-KEY", "SECRET-KEY")
from similarity.annoy_lookups import search_spans
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

from dotenv import load_dotenv
load_dotenv()
import os
wiki_pages_path = os.environ.get("wiki_pages_data")
wiki_pages_index = os.environ.get("wiki_pages_index")

with open(wiki_pages_path) as f:
    pages = json.load(f)


def papers_search(q):
    full_text_papers_query = "SELECT arxiv_id,title,authors,num_citations,abstract,url_abs,date FROM papers where arxiv_id is not null AND num_citations is not null AND title @@ to_tsquery('{}') ORDER BY num_citations DESC LIMIT 10;".format(" & ".join(q.split(" ")))
    query_res = engine.execute(full_text_papers_query).fetchall()
    res = []
    for row in query_res:
        if type(row[2]) == str:
            authors = json.loads(row[2])
        else:
            authors = row[2]
        res.append({
        "arxiv_id": row[0],
        "title": row[1],
        "authors": authors,
        "num_citations": row[3],
        "abstract": row[4],
        "url_abs": row[5],
        "date": row[6]
    })
    return {
        "results": res
    }


def wiki_pages_search(q):
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    query_vec = model.encode(q,device='cpu',convert_to_numpy=True)
    f=768
    u = AnnoyIndex(f, 'angular')
    u.load(wiki_pages_index) # super fast, will just mmap the file
    search = u.get_nns_by_vector(query_vec, 5,include_distances=True) 
    # print(search[1])  
    # for x in search:
    #     print(papers[x]) 
    labels = [pages[x]for x in search[0]]
    scores = search[1]
    # if(results[0]['arxiv_id'] == arxiv_id):
    #     results.pop(0)
    
    results_list =  {
        "results": labels,
        "scores": scores
    }
    # try:
    #     if abs(results_list['scores'][0] - results_list['scores'][1]) <= 0.1:
    #         if (results_list['labels'][0].get('type') is not None) and (results_list['labels'][1].get('type') is None):
    #             results_list['labels'][0], results_list['labels'][1] = results_list['labels'][1], results_list['labels'][0]
    #         # if results_list['labels'][0].get('type',None) == 'cskg' and results_list['labels'][1].get('type',None) == None:
                
    # except Exception as e:
    #     print(e)
    #     pass
    return results_list

# from IR.wikipedia import get_wikipedia_page

@router.get("/api/search")
async def search(q:str, description:str=None, n:int=10,intent:str=None):

    if intent == "papers":
        return papers_search(q)
    # if intent == "wikipedia":
    #     return get_wikipedia_page(q,description)
    else:
        return wiki_pages_search(q)


    return q

if __name__ == "__main__":
    print(papers_search("deep learning"))