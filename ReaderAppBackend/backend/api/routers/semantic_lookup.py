import numpy as np
import torch
import os
import pandas as pd
import faiss
import time
from sentence_transformers import SentenceTransformer
import json
import time

#f = open('/Users/diego/Documents/Projects/knowledge_system/knowledge_engine/papers/data/spans_v3.json')
#data = json.load(f)
# Get array of all labels
#labels = []
#for i in data:
#    label = i.get('label')
#    labels.append(label)

def create_index(name,data:list):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    encoded_data = model.encode(data)
    print("Building faiss index")
    print(encoded_data.shape)

    index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    index.add_with_ids(encoded_data, np.array(range(0, len(data))))

    faiss.write_index(index, name)

# distilbert-base-nli-mean-tokens
# create_index('spans_index',labels)
print("Loading model")
model = SentenceTransformer('all-MiniLM-L6-v2')

#print("Loading faiss index")

#index = faiss.read_index('/Users/diego/Documents/Projects/knowledge_system/knowledge_engine/papers/data/spans_index_V3')

def search(query,k=5):
   t=time.time()
   print("Heelo World")
   query_vector = model.encode([query])
   print("Query Vector")
   top_k= index.search(query_vector, k)
   D, I = index.search(query_vector, k)
#    print(D)
#    print(I)
#    print('totaltime: {}'.format(time.time()-t))
#    print(top_k)

   return {
    "methods": [data[_id] for _id in top_k[1].tolist()[0]],
    "scores": D
}
#    [names[_id] for _id in top_k[1].tolist()[0]]

import re
# latex_collection = db['latex_processed']
# papers = list(latex_collection.find({}))
from routers.paper import Paper
def filter_stopwords(text):
    import re
    import nltk
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    # remove numbers
    text = re.sub(r'\d+', '', text)
    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text


from similarity.annoy_lookups import search_spans
# full_text = papers[1]['full_text']
#filter stopwords and numbers
def entity_lookup(title,abstract,full_text=""):
    """
    Lookup entities in the paper
    #Parameters:
    ####    title (str): title of the paper
    ####   abstract (str): abstract of the paper
    ####    full_text (str): full text of the paper
    """
    if full_text == None:
        full_text = ""
    print(len(full_text))
    acronyms = re.findall(r"\b[A-Z]{2,}\b", full_text)

    # print(acronyms)
    # test = re.findall(r"\(([^()]+)\)", full_text)
    test = re.findall(r"\b(?:[A-Z][a-z]*){2,}", full_text)
    # remove duplicates 
    test = list(dict.fromkeys(test))
    # print(test)
    # append acronyms to test
    test.extend(acronyms)
    # remove duplicates
    test = list(dict.fromkeys(test))
    acronyms = [x for x in test if "FORMULA" not in x]
    # print(acronyms)
    full_text = filter_stopwords(full_text)
    paper = {
        "title": title,
        "abstract": abstract,
        "full_text": full_text,
    }
    paper_doc = Paper(paper,"both")

    candidates = []
    for x in paper_doc.get_semantic_chunks():
        candidates.append(x)
    for x in paper_doc.get_syntactic_chunks():
        candidates.append(x)
    #Remove candidates that are 1 word long
    candidates = [x for x in candidates if len(x.split(' ')) > 2]

    #Add acronyms to the list of candidates
    for acronym in acronyms:
        candidates.append(acronym)
    # Remove duplicate candidates

    candidates = list(dict.fromkeys(candidates))
    results_list = []
    for candidate in candidates:
        results=search_spans(candidate)
        
        top_score = results['scores'][0]
        # print(results['scores'])
        
        # If the score is high enough, add the candidate to the list
        if top_score <= 0.75:
            results_list.append({
                "span": candidate,
                "link": results['labels'][0]
            })

   
        # if 
    
    # try:
    #     if abs(results_list['scores'][0] - results_list['scores'][1]) <= 0.1:
        
    #         if results_list['labels'][0].get('type',None) == 'cskg' and results_list['labels'][1].get('type',None) == None:
    #             results_list['labels'][0], results_list['labels'][1] = results_list['labels'][1], results_list['labels'][0]
    # except Exception as e:
    #     print(e)
    #     pass
    return results_list
    #for span in spans
    # return 



# print('self supervised learning')
# query=str('self supervised learning')
# results=search(query)
# print(results[0])
# print('results :')
# for result in results:
#    print('\t',result)

def dygieDocLookup(i):
    methods = i['dygie_results']['methods']
    tasks = i['dygie_results']['tasks']
    terms = i['dygie_results']['terms']
    metrics = i['dygie_results']['metrics']
    materials = i['dygie_results']['materials']
    # remove duplicate methods
    print(len(methods))
    methods = list(dict.fromkeys(methods))
    print(len(methods))
    for method in methods:
        results=search(method)
        top_score = results['scores'][0][0]
        if top_score >= 0.75:
            print("Method: ", method)
            print("\t", results['methods'][0]['label'] + ": " + results['methods'][0]['type'])
            print("\t", results['scores'][0][0])
    for task in tasks:
        results=search(task)
        top_score = results['scores'][0][0]
        if top_score >= 0.75:
            print("Task: ", task)
            print("\t", results['methods'][0]['label'] + ": " + results['methods'][0]['type'])
            print("\t", results['scores'][0][0])
    for material in materials:
        results=search(material)
        top_score = results['scores'][0][0]
        if top_score >= 0.75:
            print("Task: ", material)
            print("\t", results['methods'][0]['label'] + ": " + results['methods'][0]['type'])
            print("\t", results['scores'][0][0])
# extracted = list(extracted.find({ "dygie_results": { "$exists": True, "$ne": None } },{'dygie_results':1}))
# for i in extracted:
#     dygieDocLookup(i)


def dygieAllTermsLookup():
    for term in all_terms:
        results=search(term)
        top_score = results['scores'][0][0]
        if top_score >= 0.75:
            print("Term: ", term)
            print("\t", results['methods'][0]['label'] + ": " + results['methods'][0]['type'])
            print("\t", results['scores'][0][0])


# class Spans:
#     span: str

#     categories: List[str] = field(default_factory=list)
#     datasets: List[Dataset] = field(default_factory=list)
#     subtasks: List["Task"] = field(default_factory=list)
#     synonyms: List[str] = field(default_factory=list)
#     source_link: Link = None


# if __name__ == "__main__":
    # create_index('spans_index',labels)
    # extracted = list(extracted.find({ "dygie_results": { "$exists": True, "$ne": None } },{'dygie_results':1}))

    # from dygie_methods import isBlankNode


    # all_terms = []
    # for node in extracted[0]['dygie_results']['all_nodes']:
    #     if(node[1]=="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
    #         all_terms.append(node[0])
    #     else:
    #         print(node)
    # # Remove duplicates from all_terms
    # print(len(all_terms))
    # all_terms = list(dict.fromkeys(all_terms))
    # print(len(all_terms))


    # dygieAllTermsLookup()
