__author__ = 'Naheed'

from itertools import combinations
import math
# from src.PointCloud import PointCloud
from src.Selector import *
from src.Filtration import RealvaluedFiltration
from src.simplex import KSimplex
import numpy as np


class WitnessStream(RealvaluedFiltration):
    def __init__(self, landmarkselector, maxdistance, numdivision, maxdimension):
        """
        This class is only for PointCloud in Euclidean space currently. Not for arbitrary Metric.
        :param landmarkselector = Selector.PointCloudSelector object
        """
        super(WitnessStream, self).__init__(np.linspace(0, maxdistance, numdivision + 1))
        # assert isinstance(landmarkselector,PointCloudSelector)
        self.pointcloud = landmarkselector.getDataPoints()
        if landmarkselector.isEmptyLandmarkset():
            landmarkselector.select()
        self.landmarkset = landmarkselector.getLandmarkPoints()
        self.landmarkindices = landmarkselector.getLandmarkindices()
        #assert isinstance(self.landmarkset, PointCloud)
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        # # Compute the distance matrix of dimension |landmarkset|x|pointcloud|
        # if landmarkselector.pointcloud.distmat is None:
        #     landmarkselector.pointcloud.compute_distancematrix()
        # print 'len: ', landmarkselector.pointcloud.distmat.shape
        self.dist_landmarkstoPointcloud = landmarkselector.getLandmark_Witness_matrix()
        self.distmat = landmarkselector.getDistanceMatrix()

    def construct(self):
        """
        Constructs the Witness Filtration/Stream.
        """
        maxcardinality_simplex = [self.maxdim + 1, self.landmarkset.size][
            self.maxdim < 0 | self.maxdim >= self.landmarkset.size]  # maximum cardinality of a KSimplex object
        # print maxcardinality_simplex
        # Construct a KDtree for nearest neighbor query
        distances = self.getNearestNeighbours(maxcardinality_simplex)
        # print 'shape: ', distances.shape
        if maxcardinality_simplex > 0:
            # First, Add all the landmark points as 0-simplex to 0-filtration
            for landmarkpoint in self.landmarkindices:
                self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[landmarkpoint]))

        if maxcardinality_simplex > 1:
            # Add an edge [ab] if there exists a p in pointcloud such that
            # max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            # Find the edges which satisfy the conditions
            for i, index_a in enumerate(self.landmarkindices):
                for index_b in xrange(i + 1, self.landmarkset.size):
                    # Check whether (index_a,index_b) can be a simplex
                    tmin = np.inf
                    potential_simplex_indices = [index_a, self.landmarkindices[index_b]]
                    # potential_simplex = [self.landmarkset.points[i], self.landmarkset.points[index_b]]
                    # print 'testing: ',potential_simplex
                    for index_z, z in enumerate(self.pointcloud):
                        check_value = self.getMaxDistance(index_z, potential_simplex_indices) - distances[index_z][1]
                        if check_value <= self.maxdist:
                            tmin = max(min(check_value, tmin), 0.0)  # incase min(check_value,tmin) <0

                    if tmin < np.inf:
                        new_simplex = KSimplex(potential_simplex_indices, degree=tmin)
                        filtration_val = tmin
                        filtration_indx = math.ceil(
                            tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                        self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                          simplex=new_simplex)

        if maxcardinality_simplex > 2:
            # Add simplices of higher order
            # I need a generator function. Given a list L of length l, and a vertex v,
            # for each L choose (l-1) subsets of length l-1, it will
            # append v to it and return that as a tuple
            def getFacesContainingV(L, v):
                sz = len(L) - 1
                for subset in combinations(L, sz):
                    yield subset + (v,)

            for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):
                # Process dimension>1 simplices from lower Filtration. since, the right hand side (a min-max term)
                # of the condition is monotonically increasing.
                # This means, if a simplex sigma appears in filtration value k, its cofaces will have value >=k
                # Only consider |cardinality_cofaces|-1 dimensional simplices in the filtration
                # when we generate its coface
                for i in xrange(self.numdiv + 1):
                    # max_filtration_val = t[i]
                    for simplex in self.get_ksimplices_from_ithFiltration(cardinality_cofaces - 2, i):
                        # Compute all cofaces and check the condition
                        assert isinstance(simplex, KSimplex)
                        new_simplex_vertices = simplex.kvertices

                        a_face_is_missing = False
                        for newpt in self.landmarkindices:
                            if newpt in new_simplex_vertices:
                                continue
                            potential_simplex_indices = new_simplex_vertices + [newpt]  # this won't change simplex.kvertices list
                            # Check whether all the faces of potential_simplex_indices are present or not up until now
                            for face in getFacesContainingV(new_simplex_vertices, newpt):
                                if self.simplex_to_filtrationmap.get(face, None) is None:
                                    a_face_is_missing = True
                                if a_face_is_missing:
                                    break
                            if a_face_is_missing:
                                continue  # A face is missing from the filtration for the simplex.

                            # potential_simplex = self.pointcloud.points[potential_simplex_indices]
                            tmin = np.inf

                            for index_z, z in enumerate(self.pointcloud):  # Try to find witness
                                check_value = self.getMaxDistance(index_z, potential_simplex_indices) - distances[index_z][
                                    cardinality_cofaces - 1]
                                if tmin > check_value and check_value <= self.maxdist:
                                    tmin = check_value

                            if tmin < np.inf:
                                new_simplex = KSimplex(potential_simplex_indices, degree=tmin)
                                filtration_val = tmin
                                filtration_indx = math.ceil(
                                    tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                                self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                                  simplex=new_simplex)

    # def construct(self):
    #     """
    #     An attempt to improve the construct function
    #     Constructs the Witness Filtration/Stream.
    #     """
    #     maxcardinality_simplex = [self.maxdim + 1, self.landmarkset.size][
    #         self.maxdim < 0 | self.maxdim >= self.landmarkset.size]  # maximum cardinality of a KSimplex object
    #     # print maxcardinality_simplex
    #     # Construct a KDtree for nearest neighbor query
    #     distances = self.getNearestNeighbours(maxcardinality_simplex)
    #     # print 'shape: ', distances.shape
    #     if maxcardinality_simplex > 0:
    #         # First, Add all the landmark points as 0-simplex to 0-filtration
    #         for landmarkpoint in self.landmarkindices:
    #             self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[landmarkpoint]))
    #
    #     if maxcardinality_simplex > 1:
    #         # # Add an edge [ab] if there exists a p in pointcloud such that
    #         # # max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
    #         # # Find the edges which satisfy the conditions
    #         # for i, index_a in enumerate(self.landmarkindices):
    #         #     for index_b in xrange(i + 1, self.landmarkset.size):
    #         #         # Check whether (index_a,index_b) can be a simplex
    #         #         tmin = np.inf
    #         #         potential_simplex_indices = [index_a, self.landmarkindices[index_b]]
    #         #         potential_simplex = [self.landmarkset.points[i], self.landmarkset.points[index_b]]
    #         #         # print 'testing: ',potential_simplex
    #         #         new_simplex = None
    #         #         for index_z, z in enumerate(self.pointcloud.points):
    #         #             check_value = self.getMaxDistance(z, potential_simplex) - distances[index_z][1]
    #         #             if tmin > check_value and check_value <= self.maxdist:
    #         #                 new_simplex = KSimplex(potential_simplex_indices, degree=check_value)
    #         #                 tmin = check_value
    #         #
    #         #         if new_simplex is not None:
    #         #             filtration_val = tmin
    #         #             filtration_indx = math.ceil(
    #         #                 tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
    #         #             self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
    #         #                                               simplex=new_simplex)
    #
    #         for index_z, z in enumerate(self.pointcloud.points):
    #
    #     if maxcardinality_simplex > 2:
    #         # Add simplices of higher order
    #         # I need a generator function. Given a list L of length l, and a vertex v,
    #         # for each L choose (l-1) subsets of length l-1, it will
    #         # append v to it and return that as a tuple
    #         def getFacesContainingV(L, v):
    #             sz = len(L) - 1
    #             for subset in combinations(L, sz):
    #                 yield subset + (v,)
    #
    #         for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):
    #             # Process dimension>1 simplices from lower Filtration. since, the right hand side (a min-max term)
    #             # of the condition is monotonically increasing.
    #             # This means, if a simplex sigma appears in filtration value k, its cofaces will have value >=k
    #             # Only consider |cardinality_cofaces|-1 dimensional simplices in the filtration
    #             # when we generate its coface
    #             for i in xrange(self.numdiv + 1):
    #                 # max_filtration_val = t[i]
    #                 for simplex in self.get_ksimplices_from_ithFiltration(cardinality_cofaces - 2, i):
    #                     # Compute all cofaces and check the condition
    #                     assert isinstance(simplex, KSimplex)
    #                     new_simplex_vertices = simplex.kvertices
    #
    #                     a_face_is_missing = False
    #                     for newpt in self.landmarkindices:
    #                         if newpt in new_simplex_vertices:
    #                             continue
    #                         potential_simplex_indices = new_simplex_vertices + [
    #                             newpt]  # this won't change simplex.kvertices list
    #                         # Check whether all the faces of potential_simplex_indices are present or not up until now
    #                         for face in getFacesContainingV(new_simplex_vertices, newpt):
    #                             if self.simplex_to_filtrationmap.get(face, None) is None:
    #                                 a_face_is_missing = True
    #                             if a_face_is_missing:
    #                                 break
    #                         if a_face_is_missing:
    #                             continue  # A face is missing from the filtration for the simplex.
    #
    #                         potential_simplex = self.pointcloud.points[potential_simplex_indices]
    #                         new_simplex = None
    #                         tmin = np.inf
    #
    #                         for index_z, z in enumerate(self.pointcloud.points):  # Try to find witness
    #                             check_value = self.getMaxDistance(z, potential_simplex) - distances[index_z][
    #                                 cardinality_cofaces - 1]
    #                             if tmin > check_value and check_value <= self.maxdist:
    #                                 new_simplex = KSimplex(potential_simplex_indices, degree=check_value)
    #                                 tmin = check_value
    #
    #                         if new_simplex is not None:
    #                             filtration_val = tmin
    #                             filtration_indx = math.ceil(
    #                                 tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
    #                             self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
    #                                                               simplex=new_simplex)
    #

    def getNearestNeighbours(self, k):
        k_nearest_distances = []
        for witness_idx in xrange(len(self.pointcloud)):
            alldistances = np.copy(self.dist_landmarkstoPointcloud[:, witness_idx])
            alldistances.sort(kind='quicksort')
            k_nearest_distances.append(alldistances[0:k + 1])
        return np.array(k_nearest_distances)

    def getMaxDistance(self, point, listofpoints):
        """
        :returns maximum distance from a given point to a pointset
        :rtype: float
        """

        return max(self.distmat[point][x] for x in listofpoints)

class MetricWitnessStream:
    def __init__(self, metriclandmarkselector, maxdistance, numdivision, maxdimension):
        """
        Strong Witness Complex Class for Arbitrary metric space.
        :param landmarkselector = Selector.MetricSelector object
        """
        assert isinstance(metriclandmarkselector, MetricSelector)
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        self.dist_landmarkstoPointcloud = metriclandmarkselector.dist_subsetstoPointcloud
        self.landmarkindices = metriclandmarkselector.subsetindices
        self.inherentdim = metriclandmarkselector.inherent_dimension

    def construct(self):
        pass
