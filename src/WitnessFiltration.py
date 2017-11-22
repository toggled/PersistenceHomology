__author__ = 'Naheed'

import PointCloud as pc
import Selector as sel


class WitnessStream:
    def __init__(self, landmarkselector, maxdistance, numdivision, maxdimension):
        """
        :param landmarkselector = Selector.PointCloudSelector object
        """
        assert isinstance(landmarkselector, sel.PointCloudSelector)
        self.pointcloud = landmarkselector.pointcloud  # PointCloud object
        self.landmarkset = landmarkselector.subsetpointcloud  # PointCloud object
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        # Compute the distance matrix of dimension |landmarkset|x|pointcloud|
        self.dist_landmarkstoPointcloud = landmarkselector.distancematrix[landmarkselector.subsetindices]  # ndarray
        self.landmarkindices = landmarkselector.subsetindices

    def construct(self):
        pass


class MetricWitnessStream:
    def __init__(self, landmarkselector, maxdistance, numdivision, maxdimension):
        """
        :param landmarkselector = Selector.MetricSelector object
        """
        assert isinstance(landmarkselector, sel.MetricSelector)
        self.maxdist = maxdistance
        self.numdiv = numdivision
        self.maxdim = maxdimension
        # Compute the distance matrix of dimension |landmarkset|x|pointcloud|
        self.dist_landmarkstoPointcloud = landmarkselector.dist_subsetstoPointcloud
        self.landmarkindices = landmarkselector.subsetindices
        self.inherentdim = landmarkselector.inherent_dimension

    def construct(self):
        pass
