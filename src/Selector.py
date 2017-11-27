import PointCloud as pc
import string
import numpy as np
import DistanceMetricinput


class PointCloudSelector:
    def __init__(self, pointcloud, subsetsize, algorithm):
        assert isinstance(pointcloud, pc.PointCloud)

        self.pointcloud = pointcloud
        self.pointcloud.ComputeDistanceMatrix()

        self.subsetsize = subsetsize
        assert isinstance(algorithm, str)
        self.algorithm = algorithm
        self.subsetindices = []  # Indices of the points chosen from 2D matrix. A subset of {0,1,...,n-1}
        self.MaxMindist = None
        self.subsetpointcloud = None

    def select(self):
        if self.algorithm == "MaxminSelector":
            self.runmaxmin()
        if self.algorithm == "RandomSelector":
            self.runrandom()

    def runrandom(self):

        self.subsetindices = []
        if self.subsetsize > self.pointcloud.size:
            raise Exception("Subset size can not be more than the size of the Pointcloud")
        elif self.subsetsize == self.pointcloud.size:
            self.subsetindices = range(0, self.pointcloud.size, 1)
        else:
            self.subsetindices = np.random.choice(self.pointcloud.size, self.subsetsize, replace=False)

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.Points[self.subsetindices])

    def runmaxmin(self):
        pass

    def getLandmarkPoints(self):
        """
        :rtype a PointCloud object
        """
        self.select()
        return self.subsetpointcloud

    # BUGG
    def getdistance_subsetstoPointcloud(self):
        """
        :rtype float (farthest distance of the closest points in Landmarkset from Pointcloud)
        """
        if not self.subsetpointcloud:
            self.select()
        dist_subsetstoPointcloud = self.pointcloud.distmat[self.subsetindices]
        # Construct the closest points distance array for each x in Pointcloud
        dist_closestpoints = np.amin(dist_subsetstoPointcloud, axis=0)
        # compute max
        self.MaxMindist = np.max(dist_closestpoints)
        return self.MaxMindist

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
        self.dist_subsetstoPointcloud = []  # distance matrix for each point in the subset to the wholeset
        self.MaxMindist = None

    def select(self):
        if self.algorithm == "MaxminSelector":
            self.runmaxmin()
        if self.algorithm == "RandomSelector":
            self.runrandom()

    def runrandom(self):
        # print type(self.distancematrix)
        selectedpoints_indices = None
        if self.subsetsize > self.totalsize:
            raise Exception("Subset size can not be more than the size of the Pointcloud")
        elif self.subsetsize == self.totalsize:
            selectedpoints_indices = range(0, self.totalsize, 1)
        else:
            selectedpoints_indices = np.random.choice(range(0, self.totalsize, 1), self.subsetsize, replace=False)

        self.subsetindices = selectedpoints_indices
        self.dist_subsetstoPointcloud = self.distancematrix[selectedpoints_indices]

    def runmaxmin(self):
        pass

    def getLandmarkPoints(self):
        """
        :rtype 2Dimenstional ndarray
        """
        self.select()
        return self.dist_subsetstoPointcloud

    def getdistance_subsetstoPointcloud(self):
        """
        :rtype float (farthest distance of the closest points in Landmarkset from Pointcloud)
        """
        if not self.dist_subsetstoPointcloud:
            self.select()
        # Construct the closest points distance array for each x in Pointcloud
        dist_closestpoints = np.amin(self.dist_subsetstoPointcloud, axis=0)
        # compute max
        self.MaxMindist = np.max(dist_closestpoints)
        return self.MaxMindist
