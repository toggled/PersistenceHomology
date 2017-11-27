import numpy as np
from scipy import spatial
import scipy.io


class PointCloud(object):
    def __init__(self, matrixofPoints):
        '''
        :param matrixofPoints: 2D Array or a List of Points (1D array).
        '''
        self.Points = np.array(matrixofPoints, dtype=float)
        self.size = self.Points.shape[0]
        self.dimension = self.Points.shape[1]
        self.distmat = None

    def __getitem__(self, item):
        return self.Points.__getitem__(item)

    def ComputeDistanceMatrix(self):
        # Euclidean for now
        self.distmat = spatial.distance.squareform(spatial.distance.pdist(self.Points, metric='euclidean'))


class MatlabPointCloud(PointCloud):
    def __init__(self, matlabfilename, varname):
        """
        :param matlabfilename: A .mat file containing 2D matrix of Pointclouds. Points across row, dimension across column
        :param varname: Which variable from the .mat file contains the pointcloud
        """

        assert isinstance(matlabfilename, str)
        if not matlabfilename.endswith("mat", 0, len(matlabfilename)):
            raise Exception("Not a mat file")
        Points = None
        try:
            Points = scipy.io.loadmat(matlabfilename)[varname]
        except:
            raise Exception('incorrect variable specified.')

        super(MatlabPointCloud, self).__init__(Points)
