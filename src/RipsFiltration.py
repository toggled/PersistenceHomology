__author__ = 'Naheed'

"""
Rips filtration is completely determined by its 1-skeleton/graph.
Therefore it stores the graph across the filtration only.
This is the epsilon variant of the Rips filtration where we increase the ball around each point in the pointcloud.
This implementation is meant to be used to compute homology/cohomology since its implemented keeping in mind the
kind of functions those algorithms expects from a filtration.
"""
import numpy as np
import math
from simplex import KSimplex
from Filtration import OldRealvaluedFiltration, RealvaluedFiltration
from PointCloud import *
from itertools import combinations
from memory_profiler import profile
# class RipsFiltration(RealvaluedFiltration):
#     """
#     The implementation follows the algorithm by Afra Zomorodian in his paper 'Fast vietoris rips'
#     """
#     def __init__(self, point_cloud, numdivision, maxdimension, maxfiltervalue):
#         super(RipsFiltration, self).__init__(np.linspace(0.0, maxfiltervalue, numdivision + 1))
#         self.point_cloud = point_cloud
#         self.numdiv = numdivision
#         self.maxdim = maxdimension


class OldBruteForceRips(OldRealvaluedFiltration):
    def __init__(self, point_cloud, numdivision, maxdimension, maxfiltervalue):
        super(OldBruteForceRips, self).__init__(np.linspace(0.0, maxfiltervalue, numdivision + 1))

        self.point_cloud = point_cloud
        self.numdiv = numdivision
        self.maxdim = maxdimension
        print self.maxfiltration_val

    @profile
    def construct(self):

        maxcardinality_simplex = self.maxdim + 1
        adjacancy_list = {}

        if maxcardinality_simplex > 0:
            # First, Add all the landmark points as 0-simplex to 0-filtration
            for point_idx in xrange(self.point_cloud.size):
                self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[point_idx]))
                adjacancy_list[point_idx] = []

        # print self.__len__()

        # This actually computes neighborhood graph.
        if maxcardinality_simplex > 1:
            # Add an edge [ab] if there exists
            #   a p in pointcloud such that max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            # Find the edges which satisfy the conditions
            # print 'here'
            for i, index_a in enumerate(self.point_cloud):
                for j in xrange(i + 1, self.point_cloud.size):
                    # Checking whether (index_a,index_b) can be a simplex
                    potential_simplex_indices = [i, j]
                    # euclid_dist = np.linalg.norm(index_a - self.point_cloud[j])
                    euclid_dist = self.point_cloud.getdistance(i, j)

                    if euclid_dist <= self.maxfiltration_val:
                        new_simplex = KSimplex(potential_simplex_indices, degree=euclid_dist)

                        # compute filtration index from filtration value.
                        filtration_indx = math.ceil(euclid_dist / self.diff_filtrationval)
                        self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=euclid_dist,
                                                          simplex=new_simplex)
                        if i < j:
                            adjacancy_list[i].append((j, euclid_dist)) # Store the edge and its filtration val
                        else:
                            adjacancy_list[j].append((i, euclid_dist))
        # print 'here', self.__len__()
        if maxcardinality_simplex > 2:
            # Add simplices of higher order
            # I need a generator function. Given a list L of length l, and a vertex v,
            # for each L choose (l-1) subsets of length l-1, it will
            # append v to it and return that as a tuple
            def get_ksimplex_containingedge(L, k, e):
                """
                return cardinality k-simplex(cardinality k+1 set) simplex containing e as subtuple/edge.
                """
                assert k+1 > 2
                for v in e:
                    L.remove(v)
                for subset in combinations(L, k-1):
                    yield subset + e

            for idx_start in adjacancy_list.keys():
                for idx_end, filtration_val in adjacancy_list[idx_start]:
                    for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):

                        for sigma in get_ksimplex_containingedge(range(self.point_cloud.size), cardinality_cofaces-1, (idx_start,idx_end) ):
                            # print sigma
                            tmax = -np.inf
                            new_simplex = None
                            face_missing = False

                            for edge in combinations(sigma, 2):
                                # print edge
                                edge = [(edge[0],edge[1]), (edge[1], edge[0])][edge[0] > edge[1]]
                                edge_missing = True

                                for (end_v, filtr_val) in adjacancy_list[edge[0]]:
                                    if edge[1] == end_v:
                                        edge_missing = False
                                        tmax = max(tmax, filtr_val)
                                        break

                                if edge_missing:
                                    face_missing = True
                                    break

                            if not face_missing:
                                new_simplex = KSimplex(sigma, tmax)
                                filtration_val = tmax
                                filtration_indx = math.ceil(
                                    tmax / self.diff_filtrationval)  # compute filtration index from filtration value.
                                self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                                  simplex=new_simplex)

        # print 'here ', self.__len__()

class BruteForceRips(RealvaluedFiltration):
    def __init__(self, point_cloud, numdivision, maxdimension, maxfiltervalue):
        super(BruteForceRips, self).__init__(filtration_values=np.linspace(0.0, maxfiltervalue, numdivision + 1).tolist())

        self.point_cloud = point_cloud
        self.numdiv = numdivision
        self.maxdim = maxdimension
        print self.maxfiltration_val

    @profile
    def construct(self):

        maxcardinality_simplex = self.maxdim + 1
        adjacancy_list = {}

        if maxcardinality_simplex > 0:
            # First, Add all the landmark points as 0-simplex to 0-filtration
            for point_idx, _ in enumerate(self.point_cloud.points):
                self.add_simplex_to_filtration(KSimplex(listofvertices=[point_idx], degree=0.0))
                adjacancy_list[point_idx] = []

        # print 'here ', self.totalsimplices

        # This actually computes neighborhood graph.
        if maxcardinality_simplex > 1:
            # Add an edge [ab] if there exists
            #   a p in pointcloud such that max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            # Find the edges which satisfy the conditions
            # print 'here'

            # for i, index_a in enumerate(self.point_cloud):
            #     for j in xrange(i + 1, self.point_cloud.size):
            #         # Checking whether (index_a,index_b) can be a simplex
            #         potential_simplex_indices = [i, j]
            #         euclid_dist = self.point_cloud.getdistance(i, j)
            #
            #         if euclid_dist <= self.maxfiltration_val:
            #             new_simplex = KSimplex(potential_simplex_indices, degree=euclid_dist)
            #             new_simplex.setBoundary()
            #             # compute filtration index from filtration value.
            #             # filtration_indx = math.ceil(euclid_dist / self.diff_filtrationval)
            #             # self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=euclid_dist,
            #             #                                   simplex=new_simplex)
            #             self.add_simplex_to_filtration(new_simplex)
            #             if i < j:
            #                 adjacancy_list[i].append((j, euclid_dist)) # Store the edge and its filtration val
            #             else:
            #                 adjacancy_list[j].append((i, euclid_dist))

            for i, j in np.column_stack(np.triu_indices(self.point_cloud.size, 1)):
                # Checking whether (i,j) can be a simplex. Note that because traversing upper diagonal i<j
                potential_simplex_indices = [i, j]
                euclid_dist = self.point_cloud.getdistance(i, j)

                if euclid_dist <= self.maxfiltration_val:
                    new_simplex = KSimplex(potential_simplex_indices, degree=euclid_dist)
                    new_simplex.setBoundary()
                    # compute filtration index from filtration value.
                    # filtration_indx = math.ceil(euclid_dist / self.diff_filtrationval)
                    # self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=euclid_dist,
                    #                                   simplex=new_simplex)
                    self.add_simplex_to_filtration(new_simplex)
                    adjacancy_list[i].append((j, euclid_dist))  # Store the edge and its filtration val. Note i< j always

        print 'here ', self.totalsimplices

        if maxcardinality_simplex > 2:
            # Add simplices of higher order
            # I need a generator function. Given a list L of length l, and a vertex v,
            # for each L choose (l-1) subsets of length l-1, it will
            # append v to it and return that as a tuple
            def get_ksimplex_containingedge(L, k, e):
                """
                return cardinality k-simplex(cardinality k+1 set) simplex containing e as subtuple/edge.
                """
                assert k+1 > 2
                for v in e:
                    L.remove(v)
                for subset in combinations(L, k-1):
                    yield subset + e

            for idx_start in adjacancy_list.keys():
                for idx_end, filtration_val in adjacancy_list[idx_start]:
                    for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):

                        for sigma in get_ksimplex_containingedge(range(self.point_cloud.size), cardinality_cofaces-1, (idx_start, idx_end) ):
                            # print sigma
                            tmax = -np.inf
                            face_missing = False

                            for edge in combinations(sigma, 2):
                                # print edge
                                edge = [(edge[0], edge[1]), (edge[1], edge[0])][edge[0] > edge[1]]
                                edge_missing = True

                                for (end_v, filtr_val) in adjacancy_list[edge[0]]:
                                    if edge[1] == end_v:
                                        edge_missing = False
                                        tmax = max(tmax, filtr_val)
                                        break

                                if edge_missing:
                                    face_missing = True
                                    break

                            if not face_missing:
                                new_simplex = KSimplex(sigma, tmax)
                                new_simplex.setBoundary()
                                self.add_simplex_to_filtration(new_simplex)

        # print 'here ', self.totalsimplices