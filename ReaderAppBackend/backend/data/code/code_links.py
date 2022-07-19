# JSON formatted string for code column in papers table
import json
import psycopg2

with open("../../downloads/links-between-papers-and-code.json", "r") as f:
    links = json.load(f)

all_keys = []
# for link in links:
#     for key in link.keys():
#         if key not in all_keys:
#             all_keys.append(key)

for link in links:
    code_link = {
        "repo_url": link["repo_url"],
        "is_official": link["is_official"],
        "mentioned_in_paper": link["mentioned_in_paper"],
        "mentioned_in_github": link["mentioned_in_github"],
        "paper_title": link["paper_title"],
        "paper_arxiv_id": link["paper_arxiv_id"],
    }
    conn = psycopg2.connect("dbname=research_papers user=diego host=165.232.156.229 password=83o2Zw5GKzMQiH923u2OzKBHCZNUw")
    cur = conn.cursor()
    sql_template = "UPDATE papers SET code = {} WHERE arxiv_id = {}".format(json.dumps(code_link), link["paper_arxiv_id"])
    cur.execute(sql_template)
    conn.commit()
    conn.close()
    print("Updated code for paper {}".format(link["paper_arxiv_id"]))
    break
#    "repo_url": "https://github.com/bfelbo/deepmoji",
#     "is_official": true,
#     "mentioned_in_paper": true,
#     "mentioned_in_github": true,
#     "framework": "tf"