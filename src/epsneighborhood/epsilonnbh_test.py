__author__ = 'Naheed'

from epsilonnbh import create_snapgraph, create_epsilon_neighbors
import networkx as nx
import matplotlib.pyplot as plt

G = create_snapgraph("/Users/naheed/NetBeansProjects/Dexa-Paper Dataset/tiny.edges")
# nx.draw(G,with_labels = 1)
# plt.show()

# print max([G.degree(str(i)) for i in range(0,34)])

# for x  in create_epsilon_neighborhood(G,2):
#     print x
print create_epsilon_neighbors(G, 2, 1)
