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
        """
        construct max min landmarks set
        """
        import random
        mindist_ptolandmarkset = np.full(self.pointcloud.size, np.inf)
        self.subsetindices = []
        for i in range(self.subsetsize + 1):

            if i == 0:
                selected_index = random.randint(0, self.pointcloud.size - 1)
                self.subsetindices.append(selected_index)
                # update min for all the rest indices
                # update min for this index to 0.
                for z in range(self.pointcloud.size):
                    # if z == selected_index:
                    #     mindist_ptolandmarkset[z] = 0.0
                    # else:
                    mindist_ptolandmarkset[z] = self.pointcloud.distmat[selected_index][z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in range(self.pointcloud.size):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.pointcloud.distmat[selected_index][z])

            self.subsetindices.append(selected_index)

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.Points[self.subsetindices])


    def getLandmarkPoints(self):
        """
        :rtype a PointCloud object
        """
        self.select()
        return self.subsetpointcloud

    def get_maxdistance_landmarktoPointcloud(self):
        """
        Computes max_z in Pointcloud d(z,L) where d(z,L) = min_l in L(Dist(z,l)
        :rtype float (farthest distance of the closest points in Landmarkset from Pointcloud)
        """
        if self.subsetpointcloud is None:  # Make sure tat the landmark set is already constructed.
            self.select()
        landmarktopointcloud_dist = self.pointcloud.distmat[self.subsetindices]  # extract distance matrix
        self.MaxMindist = np.max(np.min(landmarktopointcloud_dist, axis=0))  # Compute max of the min of each column

        return self.MaxMindist

class MetricSelector:
    def __init__(self, distancematrixobj, subsetsize, algorithm):
        """
        :param: An object, The object should be of DistanceMetricinput.DistanceMetricIn class (this class allows any matlab 2D NxN matrix as input)
        :param An integer, Number of Landmark points to be selected
        :param A string, either "MaxminSelector" or "RandomSelector"
        """
        assert isinstance(distancematrixobj, DistanceMetricinput.DistanceMetricIn)
        self.distancematrix = distancematrixobj.distance_matrix
        self.inherent_dimension = distancematrixobj.dim
        self.totalsize = distancematrixobj.size
        self.subsetsize = subsetsize
        assert subsetsize <= self.totalsize  # number of landmarks can not be larger than the size of the matrix
        assert isinstance(algorithm, str)
        self.algorithm = algorithm
        self.subsetindices = []  # Indices of the points chosen from 2D matrix. The landmark points
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
        import random
        mindist_ptolandmarkset = np.full(self.totalsize, np.inf)
        self.subsetindices = []
        for i in range(self.subsetsize + 1):

            if i == 0:
                selected_index = random.randint(0, self.pointcloud.size - 1)
                self.subsetindices.append(selected_index)
                # update min for all the rest indices
                # update min for this index to 0.
                for z in range(self.pointcloud.size):
                    # if z == selected_index:
                    #     mindist_ptolandmarkset[z] = 0.0
                    # else:
                    mindist_ptolandmarkset[z] = self.pointcloud.distmat[selected_index][z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in range(self.pointcloud.size):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.pointcloud.distmat[selected_index][z])

            self.subsetindices.add(selected_index)

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.Points[self.subsetindices])

    def getLandmarkPoints(self):
        """
        :rtype 2Dimenstional ndarray
        """
        self.select()
        return self.dist_subsetstoPointcloud

    def get_maxdistance_landmarktoPointcloud(self):
        """
        :rtype float (farthest distance of the closest points in Landmarkset from Pointcloud)
        """
        if not self.subsetindices:  # if landmarks are not constructed already
            self.select()
        # Construct the closest points distance array for each x in Pointcloud
        dist_closestpoints = np.amin(self.dist_subsetstoPointcloud, axis=0)
        # compute max
        self.MaxMindist = np.max(dist_closestpoints)
        return self.MaxMindist
