"""
This module contains class to create Lazy/Week Witness Filtration with specified parameter.
"""
__author__ = 'Naheed'

import math
from itertools import combinations
import numpy as np
from WitnessFiltration import WitnessStream
from simplex import KSimplex
import networkx as nx
from memory_profiler import profile

class WeakWitnessStream(WitnessStream):
    """
    Given a selector and other required parameters for Filtration, this class offers the
    functionality of a Weak/Lazy witness filtration.
    """
    def __init__(self, mu, landmarkselector, maxdistance, numdivision, maxdimension):
        """
        Weakwitness stream has a mu parameter. mu= number of nearest neighbor to consider.
        """
        super(WeakWitnessStream, self).__init__(landmarkselector, maxdistance, numdivision, maxdimension)
        self.mu = mu

    # @profile
    def construct(self):
        """
        Constructs the Weak Witness Filtration/Stream. Weak Witness Complex is completely specified by its 1-Skeleton.
        A simplex of higher order appears only if all its edges appears.
        """
        maxcardinality_simplex = [self.maxdim + 1, self.landmarkset.size][
            self.maxdim < 0 | self.maxdim >= self.landmarkset.size]  # maximum cardinality of a KSimplex object
        distances = self.getKthNearestNeighbour(self.mu)
        nbr_graph = nx.Graph()
        # if maxcardinality_simplex > 0:
        #     # First, Add all the landmark points as 0-simplex to 0-filtration
        #     for landmarkpoint in self.landmarkindices:
        #         self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[landmarkpoint]))

        # First, I build an |V|x|V| matrix of appearence time for each edge.
        # A simplex of higher order appears in the max of those appearnce time.

        # edge_appear_matrix = np.full((self.landmarkset.size,self.landmarkset.size),np.inf)
        if maxcardinality_simplex > 1:
            # Add an edge [ab] if there exists
            #   a p in pointcloud such that max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            # Find the edges which satisfy the conditions
            for i, index_a in enumerate(self.landmarkindices):
                j = i + 1
                while j < self.landmarkset.size:

            # for i, index_a in enumerate(self.landmarkindices):
            #     for index_b in xrange(i + 1, self.landmarkset.size):
                    # Checking whether (index_a,index_b) can be a simplex
                    tmin = np.inf
                    potential_simplex_indices = [index_a, self.landmarkindices[j]]
                    # print 'testing: ',potential_simplex
                    for index_z, _ in enumerate(self.pointcloud):
                        check_value = self.getMaxDistance(index_z, potential_simplex_indices) - distances[index_z]
                        if check_value <= self.maxdist:
                            tmin = max(min(check_value, tmin), 0.0) # incase min(check_value,tmin) <0

                    if tmin < np.inf:
                        # new_simplex = KSimplex(potential_simplex_indices, degree=tmin)
                        # filtration_val = tmin
                        # filtration_indx = math.ceil(
                        #     tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                        # self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                        #                                   simplex=new_simplex)
                        nbr_graph.add_edge(index_a, self.landmarkindices[j], filtration=tmin)
                    j += 1

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
                """
                Add cofaces of the simplex tau, where N is the set of vertices not in tau but has edge with some vertex in tau.
                """
                new_simplex = KSimplex(list(tau), degree=getdegree(tau))
                if len(tau) > 1:
                    new_simplex.setBoundary()
                self.add_simplex_to_filtration(new_simplex)
                print self.totalsimplices
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

        # if maxcardinality_simplex > 2:
        #     # Adding simplices of higher order
        #     for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):
        #         for i in xrange(self.numdiv + 1):
        #             # max_filtration_val = t[i]
        #             for simplex in self.get_ksimplices_from_ithFiltration(cardinality_cofaces - 2, i):
        #                 # Compute all cofaces and check the condition
        #                 assert isinstance(simplex, KSimplex)
        #                 new_simplex_vertices = simplex.kvertices
        #                 tmax = 0.0
        #                 threshold = simplex.degree
        #
        #                 for newpt in self.landmarkindices:
        #                     edge_missing = False
        #                     if not simplex.hasVertex(newpt):
        #                         for v in new_simplex_vertices:
        #                             edge = [newpt, v]
        #                             if edge[0] > edge[1]:
        #                                 edge[0], edge[1] = edge[1], edge[0]
        #                             edge_fil_val = self.getEdgefiltration_val(tuple(edge))
        #                             if edge_fil_val == np.inf:
        #                                 edge_missing = True
        #                                 break
        #                             else:
        #                                 tmax = max(max(tmax, edge_fil_val), threshold)
        #
        #                         if tmax <= self.maxdist and not edge_missing:
        #                             filtration_val = tmax
        #                             new_simplex = new_simplex_vertices[:]
        #                             new_simplex.append(newpt)
        #                             filtration_indx = math.ceil(
        #                                 tmax / self.diff_filtrationval)  # compute filtration index from filtration value.
        #                             self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
        #                                                               simplex=KSimplex(new_simplex))

    # def getEdgefiltration_val(self, edge):
    #     """
    #     :param edge as a tuple
    #     """
    #     val = self.simplex_to_filtrationmap.get(edge, None)
    #     if val is None:
    #         return np.inf  # never occured
    #     return val

    def getKthNearestNeighbour(self, k):
        """
        :param k : a positive integer (which nearest neighbor we want)
        :return the list of distances to the k-th nearest neighbor for the points in the pointcloud
        """
        k_nearest_distances = []
        for witness_idx, _ in enumerate(self.pointcloud):
            alldistances = np.copy(self.dist_landmarkstoPointcloud[:, witness_idx])
            alldistances.sort(kind='quicksort')
            k_nearest_distances.append(alldistances[k])
        return np.array(k_nearest_distances)
