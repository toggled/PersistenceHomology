import PointCloud as pc
import numpy as np
import DistanceMetricinput
import networkx as nx


class PointCloudSelector:
    def __init__(self, pointcloud, subsetsize, algorithm):
        assert isinstance(pointcloud, pc.PointCloud)

        self.pointcloud = pointcloud
        self.pointcloud.compute_distancematrix()

        self.subsetsize = subsetsize
        assert isinstance(algorithm, str)
        self.algorithm = algorithm
        self.subsetindices = []  # Indices of the points chosen from 2D matrix. A subset of {0,1,...,n-1}
        self.MaxMindist = None
        self.subsetpointcloud = None

    def getDataPoints(self):
        """
        return the Datapoints
        """
        return self.pointcloud

    def isEmptyLandmarkset(self):
        """
        return true if Landmarkset is empty
        """
        return self.subsetpointcloud is None

    def getDistanceMatrix(self):
        """
        Return the whole NxN matrix, n = |Landmarks|, N = |Point Cloud|
        """
        return self.pointcloud.distmat

    def getLandmark_Witness_matrix(self):
        """
        return n x N matrix, n = |Landmarks|, N = |Point Cloud|
        """
        return np.copy(self.pointcloud.distmat[self.subsetindices])  # ndarray

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

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.points[self.subsetindices])

    def runmaxmin(self):
        """
        construct max min landmarks set
        """
        import random
        mindist_ptolandmarkset = np.full(self.pointcloud.size, np.inf)
        self.subsetindices = []
        for i in xrange(self.subsetsize):
            if i == 0:
                selected_index = random.randint(0, self.pointcloud.size - 1)
                # update min for all the rest indices
                # update min for this index to 0.
                for z in xrange(self.pointcloud.size):
                    # if z == selected_index:
                    #     mindist_ptolandmarkset[z] = 0.0
                    # else:
                    mindist_ptolandmarkset[z] = self.pointcloud.distmat[selected_index][z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in xrange(self.pointcloud.size):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.pointcloud.distmat[selected_index][z])

            self.subsetindices.append(selected_index)

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.points[self.subsetindices])

    def getLandmarkindices(self):
        """
        returns the indices of the landmarks
        """
        return self.subsetindices

    def getLandmarkPoints(self):
        """
        :rtype a PointCloud object
        """
        if self.subsetpointcloud is None:
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
        for i in xrange(self.subsetsize + 1):

            if i == 0:
                selected_index = random.randint(0, self.pointcloud.size - 1)
                self.subsetindices.append(selected_index)
                # update min for all the rest indices
                # update min for this index to 0.
                for z in xrange(self.pointcloud.size):
                    # if z == selected_index:
                    #     mindist_ptolandmarkset[z] = 0.0
                    # else:
                    mindist_ptolandmarkset[z] = self.pointcloud.distmat[selected_index][z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in xrange(self.pointcloud.size):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.pointcloud.distmat[selected_index][z])

            self.subsetindices.add(selected_index)

        self.subsetpointcloud = pc.PointCloud(self.pointcloud.points[self.subsetindices])

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

class GraphSelector():
    def __init__(self, graph, subsetsize, algorithm):
        import pandas as pd
        assert isinstance(graph, nx.Graph)
        self.graph = graph
        self.subsetsize = subsetsize
        assert isinstance(algorithm, str)
        self.algorithm = algorithm

        self.nodes = sorted(graph.nodes)
        table = {}
        for n in self.nodes:
            shortest_path_lengths = nx.shortest_path_length(graph, n)
            l = []
            for m in self.nodes:
                l.append(shortest_path_lengths.get(m, None))
            table[n] = l

        self.distmat = pd.DataFrame(table, columns=self.nodes, index=self.nodes)
        del table

        self.subsetnodes = None
        self.subsetnodes_indices = None

    def select(self):
        if self.algorithm == "MaxminSelector":
            self.runmaxmin()
        if self.algorithm == "RandomSelector":
            self.runrandom()
        if self.algorithm == "MaxdegSelector":
            self.runtopkdeg()
        if self.algorithm == "optMaxminSelector":
            self.runtoptmaxmin()
        if self.algorithm == "avoidSelector":
            self.runavoid()

    def runmaxmin(self):
        import random
        graphsize = len(self.nodes)
        mindist_ptolandmarkset = np.full(graphsize, np.inf)
        self.subsetnodes_indices = []
        i = 0
        while i < self.subsetsize:
            if i == 0:
                selected_index = random.randint(0, graphsize - 1)
                # update min for all the rest indices
                # update min for this index to 0.
                for z in xrange(graphsize):
                    # if z == selected_index:
                    #     mindist_ptolandmarkset[z] = 0.0
                    # else:
                    mindist_ptolandmarkset[z] = self.distmat.iat[selected_index, z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in xrange(graphsize):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.distmat.iat[selected_index, z])

            self.subsetnodes_indices.append(selected_index)
            i += 1

        self.subsetnodes = np.asarray(self.nodes)[self.subsetnodes_indices]

    def runtoptmaxmin(self):
        import random
        graphsize = len(self.nodes)
        mindist_ptolandmarkset = np.full(graphsize, np.inf)
        self.subsetnodes_indices = []
        initial_indices = []
        i = 0
        while i < self.subsetsize:
            if i == 0:
                selected_index = random.randint(0, graphsize - 1)
                for z in xrange(graphsize):
                    mindist_ptolandmarkset[z] = self.distmat.iat[selected_index, z]
            else:
                selected_index = np.argmax(mindist_ptolandmarkset)
                # update minimum distance for all points
                for z in xrange(graphsize):
                    mindist_ptolandmarkset[z] = min(mindist_ptolandmarkset[z],
                                                    self.distmat.iat[selected_index, z])

            initial_indices.append(selected_index)
            i += 1
        initial_nodes = self.subsetnodes = np.asarray(self.nodes)[initial_indices]
        print 'initial indices', initial_indices
        print 'initial nodes', initial_nodes

        i = 0
        while i < self.subsetsize:
            index_to_del = random.choice(initial_indices)
            initial_indices.remove(index_to_del)
            # initial_nodes.remove(self.nodes.iat[index_to_del])

            max_val = 0
            selected_index = 0
            remaining = set(range(0, self.subsetsize))-set(initial_indices)
            for indices_choice in remaining:
                min_val = float("Inf")
                for z in initial_indices:
                    if self.distmat.iat[indices_choice, z] < min_val:
                        min_val = self.distmat.iat[indices_choice, z]
                if min_val > max_val:
                    max_val = min_val
                    selected_index = indices_choice

            initial_indices.append(selected_index)
            # initial_nodes.append(self.nodes.iat[selected_index])
            i += 1

        print 'after optimization ', initial_indices

        self.subsetnodes_indices = initial_indices
        self.subsetnodes = np.asarray(self.nodes)[initial_indices]

    def runrandom(self):
        if self.subsetsize > len(self.nodes):
            raise Exception("Subset size can not be more than the size of the Pointcloud")
        elif self.subsetsize == len(self.nodes):
            self.subsetnodes_indices = range(0, len(self.nodes), 1)
        else:
            self.subsetnodes_indices = np.random.choice(len(self.nodes), self.subsetsize, replace=False)

        self.subsetnodes = np.asarray(self.nodes)[self.subsetnodes_indices]
        # print self.subsetnodes_indices
        # print self.subsetnodes
        #
        # print self.distmat
        # print self.distmat.take(self.subsetnodes_indices, axis=0)

    def runtopkdeg(self):

        node_degree_pair_list_sorted = sorted(list(self.graph.degree()), key = lambda key: key[1], reverse= True)[:self.subsetsize]
        self.subsetnodes_indices = [i for (i, j) in node_degree_pair_list_sorted]
        self.subsetnodes = np.asarray(self.nodes)[self.subsetnodes_indices]

    def runavoid(self):
        pass

    def getLandmarkPoints(self):
        """
        :rtype a PointCloud object
        """
        if self.subsetnodes is None:
            self.select()
        return self.subsetnodes

    def getLandmarkindices(self):
        """
        returns the indices of the landmarks
        """
        return self.subsetnodes_indices

    def getDataPoints(self):
        """
        return the Datapoints
        """
        return self.nodes

    def isEmptyLandmarkset(self):
        """
        return true if Landmarkset is empty
        """
        return self.subsetnodes is None


    def getDistanceMatrix(self):
        """
        Return the whole NxN matrix, n = |Landmarks|, N = |Point Cloud|
        """
        return self.distmat.as_matrix()

    def getLandmark_Witness_matrix(self):
        """
        Landmarks X Witness points distance matrix
        """
        return np.copy(self.distmat.take(self.subsetnodes_indices, axis=0))

    def get_maxdistance_landmarktoPointcloud(self):
        """
        Computes max_z in Pointcloud d(z,L) where d(z,L) = min_l in L(Dist(z,l)
        :rtype float (farthest distance of the closest points in Landmarkset from Pointcloud)
        """
        if self.subsetnodes_indices is None:  # Make sure tat the landmark set is already constructed.
            self.select()
        landmarktopointcloud_dist = self.getLandmark_Witness_matrix()
        self.MaxMindist = np.max(np.min(landmarktopointcloud_dist, axis=0))  # Compute max of the min of each column
        return self.MaxMindist