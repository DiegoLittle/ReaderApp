import requests


req= requests.get("http://localhost:8000/api/search?q=Graph&description=In TensorFlow, a computation specification. Nodes in the graph represent operations. Edges are directed and represent passing the result of an operation (a Tensor) as an operand to another operation. Use TensorBoard to visualize a graph.&intent=wikipedia")
res = req.json()

print(res)

