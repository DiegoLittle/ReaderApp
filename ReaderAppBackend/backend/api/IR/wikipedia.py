# import wikipediaapi
# import time
# import requests
# import json
# from sentence_transformers import SentenceTransformer, util
# print("Loading model")
# start = time.time()
# model = SentenceTransformer('all-MiniLM-L6-v2')
# end = time.time()
# print("Print loaded model in " + str(end-start))

# def print_sections(sections, level=0):
#     sections_arr = []
#     for s in sections:
#             # print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
#             sections_arr.append({
#                 "level":level+1,
#                 "title":s.title,
#                 "text":s.text
#             })
#             subsections = print_sections(s.sections, level + 1)
#             sections_arr.extend(subsections)
#     return sections_arr
# def get_wikipedia_page(query,description):
#     req = requests.get("https://en.wikipedia.org/w/api.php?action=opensearch&search={}&format=json".format(query))
#     res = req.json()
#     urls = res[3]
#     wiki_wiki = wikipediaapi.Wikipedia(
#             language='en',
#             extract_format=wikipediaapi.ExtractFormat.WIKI
#     )
#     def disambiguation_page(page_py,get_all_pages=False):
#         subarrays = []
#         split_pos = []
#         for index,line in enumerate(page_py.text.split("\n")):
#             if line == "":
#                 # print(line)
#                 split_pos.append(index)
#         # print(split_pos)
#         for i in range(len(split_pos)):
#             if i == len(split_pos)-1:
#                 subarrays.append([x for x in page_py.text.split("\n")[split_pos[i]:] if x != ""])
#             else:
#                 subarrays.append([x for x in page_py.text.split("\n")[split_pos[i]:split_pos[i+1]] if x != ""])
#         # print(subarrays)
#         sections = []
#         for subarray in subarrays:
#             category = subarray[0]
#             pages = subarray[1:]
#             sections.append({
#                 "category": category,
#                 "pages": pages
#             })
#         if get_all_pages:
#             all_pages = []
#             for section in sections:
#                 all_pages.extend(section['pages'])
#             return all_pages
#         return sections


#     def nearest_page(query,pages):
#         query_embed = model.encode(query, convert_to_tensor=True)
#         distances = []
#         for page in pages:
#             page_embed = model.encode(page, convert_to_tensor=True)
#             cosine_score = util.cos_sim(query_embed, page_embed)
#             distances.append(cosine_score)
#         # print(distances)
#         # print(pages)
#         # print(pages[distances.index(max(distances))])
#         return pages[distances.index(max(distances))]

#     def print_categories(page):
#         categories = page.categories
#         for title in sorted(categories.keys()):
#             print("%s: %s" % (title, categories[title]))
#     page_py = wiki_wiki.page(urls[0].split("wiki/")[-1])
#     if "may refer to:" in page_py.text:
#         all_pages = disambiguation_page(page_py,get_all_pages=True)
#         nearest = nearest_page(description,all_pages)
#         page = wiki_wiki.page(nearest.split(',')[0])
#         summary = page.summary
#         title = page.title
#         text = page.text
#         categories = [category for category in page.categories if "Article" not in category and "Commons category" not in category]
#         sections = print_sections(page.sections)
#         return {
#             "title": title,
#             "summary": summary,
#             "text": text,
#             "categories": categories,
#             "sections": sections
#         }
        
# # page = get_wikipedia_page("graph","In TensorFlow, a computation specification. Nodes in the graph represent operations. Edges are directed and represent passing the result of an operation (a Tensor) as an operand to another operation. Use TensorBoard to visualize a graph.")
# # print(page)


