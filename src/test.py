import numpy as np
import PointCloud as pc
import Selector as sel


def testpointcloud():
    matrixofpoints_inR2 = []
    mean = [0, 0]
    cov = [[1, 0], [0, 1]]
    matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    p = pc.PointCloud(matrixofpoints_inR2)
    print p.size, p.dimension
    p.ComputeDistanceMatrix()
    print p.distmat


def testMatlabPointcloud():
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    print p.dimension, p.size
    p.ComputeDistanceMatrix()
    print p.distmat


def testRandomSelector():
    # Create PointCloud
    matrixofpoints_inR2 = []
    mean = [0, 0]
    cov = [[1, 0], [0, 1]]
    matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    p = pc.PointCloud(matrixofpoints_inR2)
    # Create Selector
    s = sel.PointCloudSelector(p, 2, "RandomSelector")
    print s.getLandmarkPoints().Points


def testRandomSelectorDistanceMetricio():
    from DistanceMetricinput import DistanceMetricIn
    d_in = DistanceMetricIn('/Users/naheed/PycharmProjects/PersistenceHomology/data/dmateight.mat',
                            varname='dist_eight', dimension=2)
    print d_in.size, d_in.dim

    s = sel.MetricSelector(d_in, 4, "RandomSelector")
    print s.getLandmarkPoints()


if __name__ == "__main__":
    # testpointcloud()
    # testMatlabPointcloud()
    testRandomSelector()
    # testRandomSelectorDistanceMetricio()
