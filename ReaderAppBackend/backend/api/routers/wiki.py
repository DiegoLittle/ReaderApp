from fastapi import APIRouter
import rdflib
router = APIRouter()

from SPARQLWrapper import SPARQLWrapper, JSON

from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api



def get_same_as_resources(resource):
    sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)

    q = """
    PREFIX http: <http://www.w3.org/2011/http#>
    PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
    PREFIX cs: <http://purl.org/vocab/changeset/schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX pr: <http://purl.org/ontology/prv/core#>
    # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT ?sub ?obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE {
    { 
    cskg:""" + resource + """ ?pre ?obj 
    FILTER(isUri(?pre) && STRSTARTS(STR(?pre), STR(owl:sameAs)))
    } 

    }
    ORDER BY DESC (?sup) LIMIT 500
    """
    q = """
    PREFIX http: <http://www.w3.org/2011/http#>
    PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
    PREFIX cs: <http://purl.org/vocab/changeset/schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX pr: <http://purl.org/ontology/prv/core#>
    # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT ?sub ?obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE {
    { 
    cskg:""" + resource + """ (owl:sameAs|^owl:sameAs) ?obj 
    } 

    }
    ORDER BY DESC (?sup) LIMIT 500
    """
    links = []
    sparql.setReturnFormat(JSON)
    sparql.setQuery(q)
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))
        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            # print(r.get('pre').get('value'))
            links.append(r.get('obj').get('value'))
            # topic = r.get('obj').get('value').split('/')[-1]
            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))
    except Exception as e:
        print(e)
    return links

import re

def uri_to_label(uri):
    
    if 'ontology' in uri:
        # http://scholkg.kmi.open.ac.uk/cskg/ontology#usesMethod
        resource = uri.split('#')[-1]
        split_resource = re.findall('[A-Z][^A-Z]*', resource)
        
        split_resource.insert(0,resource.split(split_resource[0])[0])
        return ' '.join(split_resource)
    elif 'resource' in uri:
        resource = uri.split('resource/')[-1]
        return resource.replace('_', ' ')
def get_resource_triples(resource):
    sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)


    q = """
    # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    
    SELECT ?sub ?type_sub ?pre ?obj ?type_obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { ?t rdf:subject cskg:""" + resource + """ . 
    ?t rdf:subject ?sub . ?t rdf:predicate ?pre . ?t rdf:object ?obj . 
    ?sub rdf:type ?type_sub .  ?obj rdf:type ?type_obj . ?t cskg-ont:hasSupport ?sup . } 
    ORDER BY DESC (?sup) LIMIT 20
    """
    sparql.setReturnFormat(JSON)
    sparql.setQuery(q)
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))
        triples = []
        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            # print(r.get('sub').get('value'))
            pre = r.get('pre').get('value')
            
            if uri_to_label(pre) == None:
                print(pre)
                continue
            obj = r.get('obj').get('value')
            sup = r.get('sup').get('value')
            # print(sup)
            # print(r.get('type_sub').get('value'))
            # print(r.get('type_obj').get('value'))
            # print(r.get('sup').get('value'))
            res_triple = resource.replace("_"," "),uri_to_label(pre),uri_to_label(obj),sup
            triples.append(res_triple)
            
            # ?sub ?type_sub ?pre ?obj ?type_obj ?sup

            # links.append(r.get('obj').get('value'))
            # topic = r.get('obj').get('value').split('/')[-1]
            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))
        return triples
    except Exception as e:
        print(e)
# from keytotext import pipeline
# nlp = pipeline('k2t')
# kws_text = nlp(t)
# print(kws_text)
from similarity.annoy_lookups import search_terms
from similarity.annoy_lookups import search_spans
import sys
sys.path.append('../')
# from ml_models.UnifiedSKG.unifiedskg_dart import run,run_batch 
import json
from pymongo import MongoClient

conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
pages = db['pages']

from thefuzz import fuzz
from Levenshtein import distance
@router.get("/api/wiki")
async def get_wiki_data(q:str):
    page = pages.find_one({
        'title':{
            '$regex' : '^{}$'.format(q),
            '$options' : 'i'}
        
    },
    {'_id': 0}
    )
    print(page==None)
    if page:
        print(page)
        page['error'] = False
        return page
    else:
        closest = search_terms(q)
        labels = [item['name'] for item in closest['labels']]
        for label in labels:
            print(label)
            print(q)
            acronyms = re.findall(r"\b[A-Z]{2,}\b", label)
            print(acronyms)
            print(distance(q,label))
            q = q.replace("-"," ")
            q = q.replace("_"," ")

            if distance(q,label)<3:
                page = pages.find_one({
                    'title':{
                        '$regex' : '^{}$'.format(label),
                        '$options' : 'i'}
                    
                },
                {'_id': 0}
                )
                if page:
                    page['error'] = False
                    return page
        # for x in closest[]
        page= {
            'error':True,
            "message": "Couldn't Find This Page",
            "suggestions":search_terms(q)
        }
        return page
    # print(res)
    # spans_res = search_spans(q)
    # print(spans_res)

    return res


    # print(q)
    # triples = get_resource_triples(q)
    # triples = [t[:-1] for t in triples]
    # num_triples = 1
    # print(len(triples)/num_triples)
    # for i in range(int(len(triples)/num_triples)):
    #     res = run_batch(triples[i*num_triples:i*num_triples+num_triples])
    #     print(res)

        
    return res
    links = get_same_as_resources(q)
    # print(links)
    if len(links) == 0:
        sparql_query(q)
        # print(broader(q))

    for link in links:
        print(link)
        if "wiki" in link:
            item = {}
            id = link.split('/')[-1]
            entity_dict = get_entity_dict_from_api(id)
            entity = WikidataItem(entity_dict)
            item["id"] = id
            item["label"] = entity.get_label()
            item["description"] = entity.get_description()
            item["aliases"] = entity.get_aliases()
            item["sitelinks"] = entity.get_sitelinks()
            item['wikipedia_link'] = entity.get_sitelinks()["enwiki"]["url"]
            
            return item
            
        
        # claim_groups = entity.get_truthy_claim_groups()
        # P349_claim = claim_groups["P349"]
        # for x in P349_claim:
        #     print(x)
        # claim_id = P349_claim[0].mainsnak.datavalue.value
        # entity = WikidataItem(get_entity_dict_from_api(claim_id))
        



def sparql_query(resource):

    sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        """
        # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?pre ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { 
    ?t rdf:subject cskg:""" + resource + """ .
    ?t rdf:predicate ?pre .
        ?t rdf:object ?obj .
        } 
    ORDER BY DESC (?sup) 
        """
    )
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))
        narrower_resources = []
        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            pre = r.get('pre').get('value')
            obj = r.get('obj').get('value')
            # topic = r.get('obj').get('value').split('/')[-1]

            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))


        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)


def broader(resource):
    sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        """
        # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?pre ?obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { 
    ?t rdf:subject cskg:""" + resource + """ .
    ?t rdf:predicate skos:broader .
        ?t rdf:object ?obj .
        ?t cskg-ont:hasSupport ?sup .
        } 
    ORDER BY DESC (?sup) 
        """
    )
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))
        items = []
        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            # print(r.get('sup').get('value'))
            items.append(r.get('obj').get('value'))
            # topic = r.get('obj').get('value').split('/')[-1]

            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))


        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
    return items

import sys
if __name__ == "__main__":
    resource = sys.argv[1]
    get_wiki_data(resource)