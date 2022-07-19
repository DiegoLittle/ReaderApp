from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from SPARQLWrapper import SPARQLWrapper, XML, N3, TURTLE, JSONLD
from rdflib import Graph


sparql = SPARQLWrapper(
    "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
)


def sparql_query():

    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint
    sparql.setReturnFormat(JSON)
#     sparql.setQuery("""
# PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
# PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
# PREFIX provo: <http://www.w3.org/ns/prov#> 
# PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
 
# SELECT ?sub ?type_sub ?pre ?obj ?type_obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
# WHERE { 
# #   ?t rdf:subject ?sub . 
# #   ?t rdf:predicate ?pre .
# #    ?t rdf:object ?obj . 
# #   ?sub rdf:type cskg-ont:Material . 
# #    ?obj rdf:type ?type_obj .
# #     ?t cskg-ont:hasSupport ?sup . } 
# #   ORDER BY DESC (?sup) LIMIT 20
#             """
#     )
    get_materials_query = """
    # Example query: Select all statements about Wikipedia.  
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
    PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
    PREFIX provo: <http://www.w3.org/ns/prov#> 
    PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?sub FROM <http://scholkg.kmi.open.ac.uk/cskg> 
    WHERE { 
    ?t rdf:subject ?sub .
        ?t rdf:predicate ?pre .
        ?t rdf:object ?obj .
        ?sub rdf:type cskg-ont:Material . 
        } 
    ORDER BY DESC (?sup) LIMIT 10000
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
 
SELECT DISTINCT ?pre ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
WHERE { 
   ?t rdf:subject cskg:eda .
    ?t rdf:predicate skos:narrower .
     ?t rdf:object ?obj .
     } 
  ORDER BY DESC (?sup) 
        """
    )
    try:
        ret = sparql.queryAndConvert()
        # print(ret.decode("utf-8"))

        for r in ret["results"]["bindings"]:
            # print(r["obj"]["value"].get("value"))
            # print(r.get('type_sub').get('value'))
            # print(r.get('sub').get('value'),r.get('pre').get('value'),r.get('obj').get('value'))
            # print(r.get('pre').get('value'))
            print(r.get('obj').get('value'))
            # print(r.get("sub").get("value"),r.get("pre").get("value"),r.get("obj").get("value"))
     
        # print(ret.serialize(format="turtle"))
        # for r in ret["results"]["bindings"]:
        #     print(r)
    except Exception as e:
        print(e)
    
    
    
    # print(type(results))
    # print(results.serialize())
    # g = Graph()
    # g.parse(data=results, format="turtle")
    # for s, p, o in g:
    #     print(s, p, o)
    # print(g.serialize(format='turtle'))
    # try:
    #     ret = sparql.queryAndConvert()
    #     print(ret)
    #     for r in ret["results"]["bindings"]:
    #         print(r)
    # except Exception as e:
    #     print(e)


sparql_query()


#         """
# # Example query: Select all statements about Wikipedia.  
# PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
# PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
# PREFIX provo: <http://www.w3.org/ns/prov#> 
# PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
 
# SELECT ?sub ?obj ?type_obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
# WHERE { 
#   ?t rdf:subject cskg:wikipedia . 
#   ?t rdf:subject ?sub .
#    ?t rdf:predicate cskg-ont:materialUsedBy .
#     ?t rdf:object ?obj . 
#    ?obj rdf:type ?type_obj .
#      } 
#   ORDER 

# SELECT ?sub  ?type_sub FROM <http://scholkg.kmi.open.ac.uk/cskg> 
# WHERE { 
#   ?t rdf:subject ?sub .
#    ?t rdf:predicate cskg-ont:usesMaterial .
#     ?t rdf:object cskg:wikipedia .
#     ?sub rdf:type cskg-ont:Task . 
#     ?sub rdf:type ?type_sub .
#      } 
#   ORDER BY DESC (?sup) LIMIT 20