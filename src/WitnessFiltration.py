__author__ = 'Naheed'

import PointCloud as pc
import Selector as sel
import numpy as np
from Filtration import RealvaluedFiltration
from src.simplex import KSimplex
import math
from itertools import combinations


class WitnessStream(RealvaluedFiltration):
    def __init__(self, landmarkselector, maxdistance, numdivision, maxdimension):
        """
        :param landmarkselector = Selector.PointCloudSelector object
        """
        super(WitnessStream, self).__init__(np.linspace(0, maxdistance, numdivision + 1))
        assert isinstance(landmarkselector, sel.PointCloudSelector)
        self.pointcloud = landmarkselector.pointcloud  # PointCloud object
        if not landmarkselector.subsetpointcloud:
            landmarkselector.select()
        self.landmarkset = landmarkselector.subsetpointcloud  # PointCloud object
        self.landmarkindices = landmarkselector.subsetindices
        assert isinstance(self.landmarkset, pc.PointCloud)
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        # Compute the distance matrix of dimension |landmarkset|x|pointcloud|
        if landmarkselector.pointcloud.distmat is None:
            landmarkselector.pointcloud.ComputeDistanceMatrix()
        print 'len: ', landmarkselector.pointcloud.distmat.shape
        self.dist_landmarkstoPointcloud = np.copy(
            landmarkselector.pointcloud.distmat[landmarkselector.subsetindices])  # ndarray
        self.pointcloud.distmat = []

    def construct(self):
        """
        Constructs the Witness Filtration/Stream.
        """

        maxcardinality_simplex = [self.maxdim + 1, self.landmarkset.size][
            self.maxdim < 0 | self.maxdim >= self.landmarkset.size]  # maximum cardinality of a KSimplex object
        print maxcardinality_simplex
        # Construct a KDtree for nearest neighbor query
        distances = self.getNearestNeighbours(maxcardinality_simplex)
        print 'shape: ', distances.shape
        if maxcardinality_simplex > 0:
            # First, Add all the landmark points as 0-simplex to 0-filtration
            for landmarkpoint in self.landmarkindices:
                self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[landmarkpoint]))

        if maxcardinality_simplex > 1:
            # Add edges
            """
            Add an edge [ab] if there exists a p in pointcloud such that max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            """
            # Find the edges which satisfy the conditions
            for i, index_a in enumerate(self.landmarkindices):
                for index_b in range(i + 1, self.landmarkset.size):
                    # Check whether (index_a,index_b) can be a simplex
                    tmin = np.inf
                    potential_simplex_indices = [index_a, self.landmarkindices[index_b]]
                    potential_simplex = [self.landmarkset.Points[i], self.landmarkset.Points[index_b]]
                    # print 'testing: ',potential_simplex
                    new_simplex = None
                    for index_z, z in enumerate(self.pointcloud.Points):
                        check_value = self.getMaxDistance(z, potential_simplex) - distances[index_z][1]
                        if tmin > check_value and check_value <= self.maxdist:
                            new_simplex = KSimplex(potential_simplex_indices, degree=check_value)
                            tmin = check_value

                    if new_simplex is not None:
                        filtration_val = tmin
                        filtration_indx = math.ceil(
                            tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                        self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                          simplex=new_simplex)

        if maxcardinality_simplex > 2:
            """
            Add simplices of higher order
            """

            # I need a generator function. Given a list L of length l, and a vertex v, for each L choose (l-1) subsets of length l-1, it will
            # append v to it and return that as a tuple
            def getFacesContainingV(L, v):
                sz = len(L) - 1
                for subset in combinations(L, sz):
                    yield subset + (v,)

            for cardinality_cofaces in range(3, maxcardinality_simplex + 1):
                # Process dimension>1 simplices from lower Filtration. since, the right hand side (a min-max term) of the condition is monotonically
                # increasing. Which means, if a simplex sigma appears in filtration value k, its cofaces will have value >=k
                # Only consider |cardinality_cofaces|-1 dimensional simplices in the filtration when we generate its coface
                for i in range(self.numdiv + 1):
                    # max_filtration_val = t[i]
                    for simplex in self.get_ksimplices_from_ithFiltration(cardinality_cofaces - 2, i):
                        # Compute all cofaces and check the condition
                        assert isinstance(simplex, KSimplex)
                        new_simplex_vertices = simplex.kvertices

                        a_face_is_missing = False
                        for newpt in self.landmarkindices:
                            if newpt in new_simplex_vertices:
                                continue
                            potential_simplex_indices = new_simplex_vertices + [
                                newpt]  # this won't change simplex.kvertices list
                            # Check whether the faces of potential_simplex_indices are present or not up until now
                            for face in getFacesContainingV(new_simplex_vertices, newpt):
                                if self.simplex_to_filtrationmap.get(face, None) is None:
                                    a_face_is_missing = True
                                if a_face_is_missing:
                                    break
                            if a_face_is_missing:
                                break  # A face is missing from the filtration for the simplex containing this newpt.

                            potential_simplex = self.pointcloud.Points[potential_simplex_indices]
                            new_simplex = None
                            tmin = np.inf

                            for index_z, z in enumerate(self.pointcloud.Points):  # Try to find witness
                                check_value = self.getMaxDistance(z, potential_simplex) - distances[index_z][
                                    cardinality_cofaces - 1]
                                if tmin > check_value and check_value <= self.maxdist:
                                    new_simplex = KSimplex(potential_simplex_indices, degree=check_value)
                                    tmin = check_value

                            if new_simplex is not None:
                                filtration_val = tmin
                                filtration_indx = math.ceil(
                                    tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                                self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                                  simplex=new_simplex)

    def getNearestNeighbours(self, k):
        # nbrs = KDTree(self.pointcloud.Points, leaf_size=self.maxdim + 2, metric='euclidean')
        # nbrs_obj  = NearestNeighbors(n_neighbors=k, algorithm='ball_tree',metric='euclidean').fit(self.pointcloud.Points)
        # return nbrs_obj.kneighbors(self.pointcloud.Points)
        k_nearest_distances = []
        for witness_idx, witness_pt in enumerate(self.pointcloud.Points):
            alldistances = np.copy(self.dist_landmarkstoPointcloud[:, witness_idx])
            alldistances.sort(kind='quicksort')
            k_nearest_distances.append(alldistances[0:k + 1])
        return np.array(k_nearest_distances)

    def getMaxDistance(self, point, listofpoints, metric='euclidean'):
        """
        :returns maximum distance from a given point to a pointset
        :rtype: float
        """

        def euclideandist(pointa, pointb):
            return math.sqrt(sum((pointa - pointb) ** 2))

        if metric == 'euclidean':
            return max(euclideandist(point, x) for x in listofpoints)

class MetricWitnessStream:
    def __init__(self, metriclandmarkselector, maxdistance, numdivision, maxdimension):
        """
        :param landmarkselector = Selector.MetricSelector object
        """
        assert isinstance(metriclandmarkselector, sel.MetricSelector)
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        self.dist_landmarkstoPointcloud = metriclandmarkselector.dist_subsetstoPointcloud
        self.landmarkindices = metriclandmarkselector.subsetindices
        self.inherentdim = metriclandmarkselector.inherent_dimension

    def construct(self):
        pass
