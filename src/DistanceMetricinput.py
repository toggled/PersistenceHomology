__author__ = 'Naheed'

import scipy.io


class DistanceMetricIn:
    def __init__(self, matfile, varname, dimension):
        """
        :param A matlab .mat file holding a 2D matrix
        """
        assert isinstance(matfile, str)
        if not matfile.endswith("mat", 0, len(matfile)):
            raise Exception("Not a mat file")
        self.distance_matrix = None
        try:
            self.distance_matrix = scipy.io.loadmat(matfile)[varname]
        except:
            raise Exception('incorrect variable specified.')

        self.dim = dimension
        self.size = self.distance_matrix.shape[0]
