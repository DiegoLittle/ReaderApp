import json
# with open('resources.json','r') as f:
#     data = json.load(f)
# data = [x.replace("_"," ") for x in data]
# with open('resources_spaced.json','w') as f:
#     json.dump(data,f)
with open('resources_spaced.json','r') as f:
    data = json.load(f)


spans = [{
    "name": x,
    "type": "resource",
    "source":"cskg"
} for x in data]
with open('cskg_spans.json','w') as f:
    json.dump(spans,f)