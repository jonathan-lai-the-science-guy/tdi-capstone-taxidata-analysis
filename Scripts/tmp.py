import networkx as nx
G = nx.Graph()
for i in range(100):
    G.add_node(i)
print(G.number_of_nodes())
