import PointCloud as pc
import string
import numpy as np
import DistanceMetricinput


class PointCloudSelector:
    def __init__(self, pointcloud, subsetsize, algorithm):
        assert isinstance(pointcloud, pc.PointCloud)
        self.pointcloud = pointcloud
        if not self.pointcloud.distmat:
            self.pointcloud.ComputeDistanceMatrix()

        self.subsetsize = subsetsize
        assert isinstance(algorithm, str)
        self.algorithm = algorithm
        self.subsetindices = []  # Indices of the points chosen from 2D matrix. A subset of {0,1,...,n-1}

    def select(self):
        if self.algorithm == "MaxminSelector":
            self.runmaxmin()
        if self.algorithm == "RandomSelector":
            self.runrandom()

    def runrandom(self):

        subset = []
        if self.subsetsize > self.pointcloud.size:
            raise Exception("Subset size can not be more than the size of the Pointcloud")
        elif self.subsetsize == self.pointcloud.size:
            subset = self.pointcloud
        else:
            subset = self.pointcloud[np.random.choice(self.pointcloud.size, self.subsetsize, replace=False), :]
            self.subsetindices = subset

        self.subsetpointcloud = pc.PointCloud(subset)

    def runmaxmin(self):
        pass

    def getLandmarkPoints(self):
        """
        :rtype a PointCloud object
        """
        self.select()
        return self.subsetpointcloud


class MetricSelector:
    def __init__(self, distancematrixobj, subsetsize, algorithm):

        assert isinstance(distancematrixobj, DistanceMetricinput.DistanceMetricIn)
        self.distancematrix = distancematrixobj.distance_matrix
        self.inherent_dimension = distancematrixobj.dim
        self.totalsize = distancematrixobj.size
        self.subsetsize = subsetsize
        assert isinstance(algorithm, str)
        self.algorithm = algorithm
        self.subsetindices = []  # Indices of the points chosen from 2D matrix. A subset of {0,1,...,n-1}
        self.subsets_distancemat = []  # distance matrix of the subset pointcloud

    def select(self):
        if self.algorithm == "MaxminSelector":
            self.runmaxmin()
        if self.algorithm == "RandomSelector":
            self.runrandom()

    def runrandom(self):
        print type(self.distancematrix)
        selectedpoints_indices = None
        if self.subsetsize > self.totalsize:
            raise Exception("Subset size can not be more than the size of the Pointcloud")
        elif self.subsetsize == self.totalsize:
            selectedpoints_indices = range(0, self.totalsize, 1)
        else:
            selectedpoints_indices = np.random.choice(range(0, self.totalsize, 1), self.subsetsize, replace=False)

        self.subsetindices = selectedpoints_indices
        self.subsets_distancemat = self.distancematrix[selectedpoints_indices][:, selectedpoints_indices]

    def runmaxmin(self):
        pass

    def getLandmarkPoints(self):
        """
        :rtype 2Dimenstional ndarray
        """
        self.select()
        return self.subsets_distancemat
