import json
import pandas as pd
import requests

with open('google_ml-glossary.json','r') as f:
    data = json.load(f)

for term in data:
    res = requests.get("http://localhost:8000/api/search?q=" + term['name'])
    data = res.json()
    print(data)

