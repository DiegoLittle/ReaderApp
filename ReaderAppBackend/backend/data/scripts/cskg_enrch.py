from SPARQLWrapper import SPARQLWrapper, XML, N3, TURTLE, JSONLD,JSON
from rdflib import Graph
import json
from pymongo import MongoClient

from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
conn_str = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229"
# set a 5-second connection timeout
client = MongoClient(conn_str)
db = client['research_papers']
collection = db['entities']



sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)


def get_entity_triples(resource):
    sparql.setReturnFormat(JSON)
    q="""
            # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
    
    SELECT DISTINCT ?sub ?pre ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { 
        {
    ?t rdf:subject cskg:""" + resource + """ .
    ?t rdf:subject ?sub .
        ?t rdf:predicate ?pre .
        ?t rdf:object ?obj .
        } 
    }
    ORDER BY DESC (?sup) 
            """
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
    
    SELECT DISTINCT ?sub ?pre ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { 
        {
    cskg:""" + resource + """ ?pre ?obj .
        } 
    }
    ORDER BY DESC (?sup) 
            """
    )
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))
        semantic_links = []
        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            # sub = r.get('sub').get('value')
            pre = r.get('pre').get('value')
            obj = r.get('obj').get('value')
            if(pre == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
                resource_type = obj.split("#")[-1].lower()
            elif(pre == "http://www.w3.org/2002/07/owl#sameAs"):
                semantic_links.append(obj)
        # print(resource)
        # print(resource_type)
        # print(semantic_links)

        # print("Updated record for: ",resource)
        item = None
        for link in semantic_links:
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
                
                # return item
        if(item):

            new_values = {"$set":{
                "semantic_links":semantic_links,
                "resource_type":resource_type,
                "wikipedia_link":item['wikipedia_link'],
                "aliases":item['aliases'],
                "wiki_data":item,
            }}
        else:
            new_values = {"$set":{
                "semantic_links":semantic_links,
                "resource_type":resource_type,
            }}

        filter = { 'name': resource.replace("_"," ") }
        result = collection.update_one(filter, new_values)
        # print(result.modified_count)
        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)


def update_wiki_data(worker):
    mongo_methods = list(collection.find({
    "sources":{
        "$in":["cskg"]
    },
    "wiki_data":{ "$exists": False }
}))
    print(len(mongo_methods))
    print("Starting worker: ",worker)
    for m in mongo_methods[worker*5000:(worker+1)*5000]:
        get_entity_triples(m['name'].replace(" ","_"))

from multiprocessing import Process
import sys
def main(threads=1):
    print(threads)
    processes = []
    for i in range(threads):
        p = Process(target=update_wiki_data, args=(i,))
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