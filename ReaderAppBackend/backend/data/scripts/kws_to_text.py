from keytotext import pipeline

nlp = pipeline('k2t')
kws_text = nlp(['wikipedia','material used by','knowledge base'])
print(kws_text)