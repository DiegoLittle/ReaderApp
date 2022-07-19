import json
def get_aikg_lines():
    with open("aikg.ttl","r") as f:
        ai_kg = f.read()

    lines = [x for x in ai_kg.split("\n") if x != "" and "aikg:" in x]
    with open("aikg_lines.txt","w") as f:
        f.write("\n".join(lines))
with open("aikg_lines.txt","r") as f:
    lines = f.read().split("\n")
resources = []
for line in lines:
    res_arr = [x for x in line.split(" ") if x != "" and x != "," and x != "." and x != ";" and "aikg:" in x and "statement" not in x]
    if len(res_arr) > 0:
        resources.append(res_arr[0])

print(len(resources))
#remove duplicate resources from the list
resources = list(set(resources))
print(len(resources))
all_resources = []
for resource in resources:
    resource = resource.replace("aikg:","")
    resource_name = resource.replace("_"," ").title()
    all_resources.append({
        "name": resource_name,
        "resource_id": resource
    })
with open("aikg_resources.json","w") as f:
    json.dump(all_resources,f)


    
