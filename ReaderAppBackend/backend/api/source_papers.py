import urllib.request
import time
import feedparser
import logging
from data.data_sources.s2 import get_paper_citations
from routers.semantic_lookup import entity_lookup
logger = logging.getLogger(__name__)
import models
import psycopg2
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from cso_classifier import CSOClassifier
import pdfx
import os

cc = CSOClassifier(modules = "both", enhancement = "first", explanation = True)


q = 'cat:cs.CV+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.AI+OR+cat:cs.NE+OR+cat:cs.RO+OR+cat:cs.ir'
def get_response(search_query, start_index=0):
    """ pings arxiv.org API to fetch a batch of 100 papers """
    # fetch raw response
    base_url = 'http://export.arxiv.org/api/query?'
    add_url = 'search_query=%s&sortBy=lastUpdatedDate&start=%d&max_results=2000' % (search_query, start_index)
    #add_url = 'search_query=%s&sortBy=submittedDate&start=%d&max_results=100' % (search_query, start_index)
    search_query = base_url + add_url
    print(f"Searching arxiv for {search_query}")
    with urllib.request.urlopen(search_query) as url:
        response = url.read()

    if url.status != 200:
        print(f"arxiv did not return status 200 response")

    return response

def encode_feedparser_dict(d):
    """ helper function to strip feedparser objects using a deep copy """
    if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
        return {k: encode_feedparser_dict(d[k]) for k in d.keys()}
    elif isinstance(d, list):
        return [encode_feedparser_dict(k) for k in d]
    else:
        return d

def parse_arxiv_url(url):
    """
    examples is http://arxiv.org/abs/1512.08756v2
    we want to extract the raw id (1512.08756) and the version (2)
    """
    ix = url.rfind('/')
    assert ix >= 0, 'bad url: ' + url
    idv = url[ix+1:] # extract just the id (and the version)
    parts = idv.split('v')
    assert len(parts) == 2, 'error splitting id and version in idv string: ' + idv
    return idv, parts[0], int(parts[1])

def parse_response(response):

    out = []
    parse = feedparser.parse(response)
    for e in parse.entries:
        j = encode_feedparser_dict(e)
        # extract / parse id information
        idv, rawid, version = parse_arxiv_url(j['id'])
        j['_idv']= idv
        j['_id'] = rawid
        j['_version'] = version
        j['_time'] = time.mktime(j['updated_parsed'])
        j['_time_str'] = time.strftime('%b %d %Y', j['updated_parsed'])
        # delete apparently spurious and redundant information
        del j['summary_detail']
        del j['title_detail']
        out.append(j)

    return out
from database import engine
from utils.arxiv_categories import CATEGORIES
models.Base.metadata.create_all(bind=engine)

def getCategories(paper):
    category_ids = []
    category_ids.append(paper['arxiv_primary_category'].get('term',None))
    for x in paper['tags']:
        category_ids.append(x.get('term',None))
    # Remove duplicate category_ids
    category_ids = list(set(category_ids))
    categories = []
    for cat in category_ids:
        try:
            categories.append(CATEGORIES.get(cat).get('name'))
        except Exception as e:
            # print(e)
            # print('Error adding category')
            # print(CATEGORIES.get(cat))
            return None
    return categories

import sys
# num_pages = sys.argv[1] or 1
num_pages = 1
for i in range(int(num_pages)):
    print(f"Page {i}")
    res = get_response(q,i)
    papers = parse_response(res)
    print(len(papers))
    from database import SessionLocal, engine
    import json
    from utils.paper_lookup import arxiv_lookup
    from utils.full_text_extract import full_text,get_keywords
    retrieved_papers = []
    # print(papers[0].keys())
    for paper in papers:
        # print(paper['_id'])
        lookup = arxiv_lookup(paper['_id'])
        
        if len(lookup) > 0:
            print('Paper already in database')
            continue
            
        print(paper['_id'])
        arxiv_id = paper['_id']
        authors = []
        for a in paper['authors']:
            authors.append(a['name'])
        categories = getCategories(paper)
                
        if(len(authors)>10):
            authors = authors[:10]
        # try:
        #     # print("Extract full text")
        #     # text = full_text(arxiv_id)

        #     raise
        # except Exception as e:
        #     print(e)
        #     continue
        try:
            paper_doc = {
                "title": paper['title'],
                "abstract": paper['summary']
            }
            result = cc.run(paper_doc)
            
            # print(paper.title)
            # print(paper.keywords)
            yake_kws = get_keywords(paper['summary'])
            yake_keywords = [x[0] for x in yake_kws]
            yake_scores = [x[1] for x in yake_kws]
            cso_keywords = result['enhanced']
            all_keywords = []
            all_keywords.extend(yake_keywords)
            all_keywords.extend(cso_keywords)
            pdf = pdfx.PDFx("https://arxiv.org/pdf/{}.pdf".format(arxiv_id))
            paper_full_text = pdf.get_text()
            
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
            api_key = os.environ['S2_API_KEY']
            paper_data,citations,references = get_paper_citations(arxiv_id,api_key)
            entities = entity_lookup(paper['title'],paper['summary'],paper_full_text)
            entities = [json.dumps(e) for e in entities ]
            if 'error' in paper_data.keys():
                    print(paper_data['error'])
                    paper_data = 'error'
            else:
                num_citations = paper_data['citationCount']
                num_references = paper_data['referenceCount']
                num_influential_citations = paper_data['influentialCitationCount']
                paper_data = json.dumps(paper_data)
            # setattr(paper_query, 's2_citations', json.dumps(citations))
            # setattr(paper_query, 'refs', json.dumps(references))
            try:
                if len(references['data']) > 0:
                    refs = json.dumps(references['data'])
                else:
                    refs = None
                if len(citations['data']) > 0:
                    citations = json.dumps(citations['data'])
                else:
                    citations = None

            except KeyError:
                if 'error' in references.keys():
                    print(references['error'])
                if 'error' in citations.keys():
                    print(citations['error'])
                if 'error' in paper_data.keys():
                    print(paper_data['error'])
                pass
            
            # break
            # db = SessionLocal()
            # paper_query = db.query(models.Paper).filter(models.Paper.arxiv_id == paper['arxiv_id']).first()
            # setattr(paper_query, 's2_paper', json.dumps(paper_data))
            # setattr(paper_query, 's2_citations', json.dumps(citations))
            # setattr(paper_query, 'refs', json.dumps(references))
            # setattr(paper_query, 's2_paper', json.dumps(paper_data))
            # setattr(paper_query, 's2_citations', json.dumps(citations))
            # setattr(paper_query, 'refs', json.dumps(references))
            # print(paper_data,citations,references)
            paper_doc = models.Paper(
                id= arxiv_id,
                arxiv_id=arxiv_id,
                title= paper['title'],
                full_text = paper_full_text,
                abstract= paper['summary'],
                authors= json.dumps(authors),
                categories= json.dumps(categories),
                date= paper['published'],
                url_abs= paper['link'],
                url_pdf= paper['link'] + '.pdf',
                keywords= json.dumps(keywords_attr),
                s2_paper= paper_data,
                s2_citations = citations,
                refs = refs,
                entity_links = entities,
                num_citations = num_citations,
                num_references = num_references,
                num_influential_citations = num_influential_citations
            )
            # with open("test.json", "w") as f:
            #     json.dump(paper_doc.__dict__, f)
            db = SessionLocal()
            db.add(paper_doc)
            db.commit()
            db.close()
            print("Added paper to database: {} id {}".format(paper['title'],arxiv_id))
        except ValueError as e:
            print(e)
            print("Error in paper: {}".format(arxiv_id))
            paper_doc = models.Paper(
                id= arxiv_id,
                arxiv_id=arxiv_id,
                title= paper['title'],
                abstract= paper['summary'],
                authors= json.dumps(authors),
                categories= json.dumps(categories),
                date= paper['published'],
                url_abs= paper['link'],
                url_pdf= paper['link'] + '.pdf',
                keywords= json.dumps(keywords_attr),
                s2_paper= paper_data,
                s2_citations = citations,
                refs = refs,
                entity_links = entities,
                num_citations = num_citations,
                num_references = num_references,
                num_influential_citations = num_influential_citations
            )
            # with open("test.json", "w") as f:
            #     json.dump(paper_doc.__dict__, f)
            db = SessionLocal()
            db.add(paper_doc)
            db.commit()
            db.close()
        except IntegrityError as e:
            if(type(e.orig) == UniqueViolation):
                print("Paper already exists: {}".format(arxiv_id))
            
                db.rollback()
                db.close()
                print("Rolling back")

                continue
            else:
                raise e