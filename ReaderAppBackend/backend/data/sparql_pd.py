import sparql_dataframe


endpoint = "https://scholkg.kmi.open.ac.uk/sparqlendpoint/"
resource = "artificial_intelligence"
# q ="""
#         # Example query: Select all statements about Wikipedia.  
# PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
# PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
# PREFIX provo: <http://www.w3.org/ns/prov#> 
# PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
 
# SELECT DISTINCT ?obj FROM <http://scholkg.kmi.open.ac.uk/cskg> 
# WHERE { 
#    ?t rdf:subject cskg:""" + resource + """ .
#     ?t rdf:predicate skos:narrower .
#      ?t rdf:object ?obj .
#      } 
#   ORDER BY DESC (?sup) 
#         """
q = """
        # Example query: Select all statements about Wikipedia.  
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
PREFIX provo: <http://www.w3.org/ns/prov#> 
PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
 
SELECT DISTINCT ?obj ?obj2 FROM <http://scholkg.kmi.open.ac.uk/cskg> 
WHERE { 
   ?t rdf:subject cskg:artificial_intelligence .
    ?t rdf:predicate skos:narrower .
     ?t rdf:object ?obj .
     } 
  ORDER BY DESC (?sup) 
        """
resource = "neural_network_architecture"
q = """
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
        }
        ORDER BY DESC (?sup) 
                """
q = """
# Example query: Select all statements about Wikipedia.  
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
PREFIX provo: <http://www.w3.org/ns/prov#> 
PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
 
SELECT DISTINCT ?sub ?type_sub ?pre ?obj ?type_obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
WHERE {
{ 
  ?t rdf:subject cskg:""" + resource + """ . 
  ?t rdf:subject ?sub . 
  ?t rdf:predicate ?pre .
  ?t rdf:object ?obj . 
  ?sub rdf:type ?type_sub . 
  ?obj rdf:type ?type_obj .
    ?t cskg-ont:hasSupport ?sup . } UNION {
    { 
  ?t rdf:object cskg:""" + resource + """ . 
  ?t rdf:subject ?sub . 
  ?t rdf:predicate ?pre .
  ?t rdf:object ?obj . 
  ?sub rdf:type ?type_sub . 
  ?obj rdf:type ?type_obj .
  ?t cskg-ont:hasSupport ?sup . } 
  }
}
  ORDER BY DESC (?sup)
"""
df = sparql_dataframe.get(endpoint, q)
print(df.head())
df.to_csv("output.csv")

# 

owl_query= """
?t rdf:subject cskg:wikipedia . 
  ?t rdf:subject ?sub . 
  ?t rdf:predicate ?pre .
  ?t rdf:object ?obj . 
  ?sub rdf:type ?type_sub . 
  ?obj rdf:type ?type_obj .
    ?t cskg-ont:hasSupport ?sup .
    FILTER(isUri(?pre) && STRSTARTS(STR(?pre), STR(owl:)))
"""


