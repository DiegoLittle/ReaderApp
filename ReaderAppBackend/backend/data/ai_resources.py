from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from SPARQLWrapper import SPARQLWrapper, XML, N3, TURTLE, JSONLD
from rdflib import Graph
import json
sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)

topics = []
def recursive_narrow(resource):
    print(len(topics))
    with open('resources.json', "w") as f:
        f.write(json.dumps(topics))
    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint
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
    ?t rdf:predicate skos:narrower .
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
            # print(r.get('pre').get('value'))
            # print(r.get('obj').get('value'))
            topic = r.get('obj').get('value').split('/')[-1]
            if topic not in topics:
                topics.append(topic)
                narrower_resources.append(topic)
            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))
        for n in narrower_resources:
            sparql_query(n)
        if len(narrower_resources) == 0:
            return


        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
    return narrower_resources

def sparql_query(resource):
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
        
        SELECT DISTINCT ?sub ?pre ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
        WHERE { 
            {
        ?t rdf:subject cskg:""" + resource + """ .
        ?t rdf:subject ?sub .
            ?t rdf:predicate ?pre .
            ?t rdf:object ?obj .
            } 
        } UNION {
        ?t rdf:object cskg:""" + resource + """ .
        ?t rdf:object ?obj .
            ?t rdf:predicate ?pre .
            ?t rdf:subject ?sub .
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
            # print(r.get('pre').get('value'))
            print(r.get('obj').get('value'))


        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
    return narrower_resources
    
 
sparql_query("artificial_intelligence")
with open('ai_resources.json', 'a') as f:
    f.write(json.dumps(topics))