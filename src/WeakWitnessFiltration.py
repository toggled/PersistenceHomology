"""
This module contains class to create Lazy/Week Witness Filtration with specified parameter.
"""
__author__ = 'Naheed'

import math
from itertools import combinations
import numpy as np
from src.WitnessFiltration import WitnessStream
from src.simplex import KSimplex


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

    def construct(self):
        """
        Constructs the Weak Witness Filtration/Stream. Weak Witness Complex is completely specified by its 1-Skeleton.
        A simplex of higher order appears only if all its edges appears.
        """
        maxcardinality_simplex = [self.maxdim + 1, self.landmarkset.size][
            self.maxdim < 0 | self.maxdim >= self.landmarkset.size]  # maximum cardinality of a KSimplex object
        distances = self.getKthNearestNeighbour(self.mu)

        if maxcardinality_simplex > 0:
            # First, Add all the landmark points as 0-simplex to 0-filtration
            for landmarkpoint in self.landmarkindices:
                self.add_simplex_toith_filtration(0, 0.0, KSimplex(listofvertices=[landmarkpoint]))

        # First, I build an |V|x|V| matrix of appearence time for each edge.
        # A simplex of higher order appears in the max of those appearnce time.

        # edge_appear_matrix = np.full((self.landmarkset.size,self.landmarkset.size),np.inf)
        if maxcardinality_simplex > 1:
            # Add an edge [ab] if there exists
            #   a p in pointcloud such that max(d(a,p),d(b,p))< filtration_value + d(p,2nd nearest neighbor of p)
            # Find the edges which satisfy the conditions
            for i, index_a in enumerate(self.landmarkindices):
                for index_b in xrange(i + 1, self.landmarkset.size):
                    # Checking whether (index_a,index_b) can be a simplex
                    tmin = np.inf
                    potential_simplex_indices = [index_a, self.landmarkindices[index_b]]
                    # print 'testing: ',potential_simplex
                    for index_z, z in enumerate(self.pointcloud.points):
                        check_value = self.getMaxDistance(index_z, potential_simplex_indices) - distances[index_z]
                        if tmin > check_value and check_value <= self.maxdist:
                            tmin = max(check_value, 0)

                    if tmin < np.inf:
                        new_simplex = KSimplex(potential_simplex_indices, degree=tmin)
                        filtration_val = tmin
                        filtration_indx = math.ceil(
                            tmin / self.diff_filtrationval)  # compute filtration index from filtration value.
                        self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                          simplex=new_simplex)
        if maxcardinality_simplex > 2:
            # Adding simplices of higher order
            def getsubfaces(sigma, cardinality):
                """
                Yields cardinality sized subsets of simplex sigma
                :param sigma: a list (a simplex)
                :param cardinality: an integer less than |sigma| i.e cardinality of some subset of sigma
                :return: list
                """
                assert cardinality < len(sigma)
                for subset in combinations(sigma, cardinality):
                    yield subset

            for cardinality_cofaces in xrange(3, maxcardinality_simplex + 1):
                for newsigma in getsubfaces(self.landmarkindices, cardinality_cofaces):
                    tmax = -1
                    edge_missing = False
                    for edge in getsubfaces(newsigma,
                                            2):  # We are only checking whether the edges are there. not all the faces.
                        edge_fil_val = self.getEdgefiltration_val(edge)
                        if edge_fil_val == np.inf:
                            edge_missing = True
                            break
                        else:
                            tmax = max(tmax, edge_fil_val)
                    if tmax < 0 or edge_missing:
                        continue
                    if tmax <= self.maxdist:
                        filtration_val = tmax
                        filtration_indx = math.ceil(
                            tmax / self.diff_filtrationval)  # compute filtration index from filtration value.
                        self.add_simplex_toith_filtration(i=filtration_indx, filtration_val=filtration_val,
                                                          simplex=KSimplex(newsigma))

    def getEdgefiltration_val(self, edge):
        """
        :param edge as a tuple
        """
        val = self.simplex_to_filtrationmap.get(edge, None)
        if val is None:
            return np.inf  # never occured
        return val

    def getKthNearestNeighbour(self, k):
        """
        :param k : a positive integer (which nearest neighbor we want)
        :return the list of distances to the k-th nearest neighbor for the points in the pointcloud
        """
        k_nearest_distances = []
        for witness_idx in xrange(len(self.pointcloud.points)):
            alldistances = np.copy(self.dist_landmarkstoPointcloud[:, witness_idx])
            alldistances.sort(kind='quicksort')
            k_nearest_distances.append(alldistances[k])
        return np.array(k_nearest_distances)
