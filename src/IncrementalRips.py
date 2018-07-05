__author__ = 'Naheed'
from Filtration import RealvaluedFiltration
from simplex import KSimplex
import numpy as np
from memory_profiler import profile
import networkx as nx
from itertools import combinations

"""
Rips filtration is completely determined by its 1-skeleton/graph.
Therefore it stores the graph across the filtration only.
This is the epsilon variant of the Rips filtration where we increase the ball around each point in the pointcloud.
This implementation is meant to be used to compute homology/cohomology since its implemented keeping in mind the
kind of functions those algorithms expects from a filtration.
"""


class IncrementalRips(RealvaluedFiltration):
    def __init__(self, point_cloud, numdivision, maxdimension, maxfiltervalue):
        super(IncrementalRips, self).__init__(filtration_values=np.linspace(0.0, maxfiltervalue, numdivision + 1).tolist())

        self.point_cloud = point_cloud
        self.numdiv = numdivision
        self.maxdim = maxdimension
        print self.maxfiltration_val

    # @profile
    def construct(self):

        maxcardinality_simplex = self.maxdim + 1
        nbr_graph = nx.Graph()

        if maxcardinality_simplex > 1:
            # We compute the neighborhood graph first
            for i, j in np.column_stack(np.triu_indices(self.point_cloud.size, 1)):
                euclid_dist = self.point_cloud.getdistance(i, j)
                if euclid_dist <= self.maxfiltration_val:
                    nbr_graph.add_edge(i, j, filtration=euclid_dist)
                else:
                    nbr_graph.add_node(i)
                    nbr_graph.add_node(j)

            print 'nodes ', len(nbr_graph.nodes), ' edges ', len(nbr_graph.edges)

            def getlowerneighbor(v):
                return set([u for u in nbr_graph.neighbors(v) if u > v])

            def getdegree(tau):
                degree = 0.0
                if len(tau) == 1:
                    return degree
                elif len(tau) == 2:
                    return nbr_graph.edges[tuple(tau)]['filtration']
                else:
                    for edge in combinations(tau, 2):
                        degree = max(degree, nbr_graph.edges[edge]['filtration'])
                    return degree

            def add_cofaces(tau, N):
                new_simplex = KSimplex(list(tau), degree=getdegree(tau))
                if len(tau) > 1:
                    new_simplex.setBoundary()
                self.add_simplex_to_filtration(new_simplex)

                if len(tau) >= maxcardinality_simplex:
                    return
                else:
                    for v in N:
                        sigma = tau.union(set([v]))
                        M = N.intersection(getlowerneighbor(v))
                        add_cofaces(sigma, M)

            for u in nbr_graph.nodes:
                N = getlowerneighbor(u)
                add_cofaces(set([u]), N)
