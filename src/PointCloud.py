"""
This module contains class definitions to deal Point Cloud data coming from different sources
 (e.g. Matlab matrix, pointcloud from file, numpy matrix)
"""
import numpy as np
from scipy import spatial
import scipy.io


class PointCloud(object):
    def __init__(self, matrixofpoints):
        '''
        :param matrixofpoints: 2D Array or a List of points (1D array).
        '''
        self.points = np.array(matrixofpoints, dtype=float)
        self.size = self.points.shape[0]
        self.dimension = self.points.shape[1]
        self.distmat = None

    def __getitem__(self, item):
        return self.points.__getitem__(item)

    def compute_distancematrix(self):
        """
        Computes Euclidean Distance Matrix (for now)
        :rtype: None
        """
        self.distmat = spatial.distance.squareform(spatial.distance.pdist(self.points, metric='euclidean'))


class MatlabPointCloud(PointCloud):
    def __init__(self, matlabfilename, varname):
        """
        Class for constructing  Point cloud data created in Matlab
        :param matlabfilename: A .mat file containing 2D matrix of Pointclouds.
                Points across row, dimension across column
        :param varname: Which variable from the .mat file contains the pointcloud
        """

        assert isinstance(matlabfilename, str)
        if not matlabfilename.endswith("mat", 0, len(matlabfilename)):
            raise Exception("Not a mat file")
        points = None
        try:
            points = scipy.io.loadmat(matlabfilename)[varname]
        except:
            raise Exception('incorrect variable specified.')

        super(MatlabPointCloud, self).__init__(points)
