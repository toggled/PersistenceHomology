__author__ = 'Naheed'

import networkx as nx
import sys


def create_snapgraph(filename=None):
    G = nx.Graph()
    # filename = 'datasets/414.edges'
    with open(filename, 'r') as f:
        while 1:
            # print f.readline().split()
            line = f.readline()
            if not line:
                break
            nodea, nodeb = line.split()
            # nodea,nodeb = line.split(',')
            # if nodea == '200':
            #     G.add_node(nodea,color = 'green')
            # else:
            #     G.add_node(nodea)
            # print nodea,nodeb

            # G.add_node(nodea)
            # G.add_node(nodeb)
            G.add_edge(int(nodea), int(nodeb))

    return G


def create_epsilon_neighbors(G, maxdim=3, epsilon=2):
    """
    maxdim = maximum dimension of simplex we are gonna allow (maxdim = 3 means we ignore all >=3-simplex
    epsilon = epsilon neighbors (set of vertices which are epsilon geodesic distance away)
    """
    assert isinstance(G, nx.Graph)
    epsilon_nbs = {}
    if epsilon >= 0:
        for i in G.nodes():
            epsilon_nbs[i] = {i}

    for eps in range(1, epsilon + 1):
        seta = create_epsilon_neighbors(G, maxdim, epsilon - 1)
        # print seta
        epsilon_nbs[eps] = set({})
        for i in seta:
            epsilon_nbs[eps] |= epsilon_nbs[i]
            # print epsilon_nbs

    return epsilon_nbs
