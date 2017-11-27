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
    s = sel.PointCloudSelector(p, 5, "RandomSelector")
    print s.getLandmarkPoints().Points

    print s.getdistance_subsetstoPointcloud()

def testRandomSelectorDistanceMetricio():
    from DistanceMetricinput import DistanceMetricIn
    d_in = DistanceMetricIn('/Users/naheed/PycharmProjects/PersistenceHomology/data/dmateight.mat',
                            varname='dist_eight', dimension=2)
    print d_in.size, d_in.dim

    s = sel.MetricSelector(d_in, 4, "RandomSelector")
    print s.getLandmarkPoints()


def testMaxdist():
    from DistanceMetricinput import DistanceMetricIn
    d_in = DistanceMetricIn('/Users/naheed/PycharmProjects/PersistenceHomology/data/dmateight.mat',
                            varname='dist_eight', dimension=2)
    print d_in.size, d_in.dim

    s = sel.MetricSelector(d_in, 4, "RandomSelector")
    print s.getdistance_subsetstoPointcloud()


def testWitnessStream():
    from WitnessFiltration import WitnessStream
    from WeakWitnessFiltration import WeakWitnessStream
    # mean = [0, 0]
    # cov = [[1, 0], [0, 1]]
    # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    # p = pc.PointCloud(matrixofpoints_inR2)
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    p.ComputeDistanceMatrix()
    # Create Selector
    pointcloud_sel = sel.PointCloudSelector(p, 100, "RandomSelector")
    R = float(pointcloud_sel.getdistance_subsetstoPointcloud()) / 2
    # R = 0
    print 'R = ', R
    numdivision = 5
    maxdim = 4
    # ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision, maxdimension=maxdim)
    ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                           maxdimension=maxdim)
    ws.construct()
    print ws


def testWitnessStreamPH():
    from WitnessFiltration import WitnessStream
    from WeakWitnessFiltration import WeakWitnessStream
    from src.ComputeInterval import IntervalComputation

    # mean = [0, 0]
    # cov = [[1, 0], [0, 1]]
    # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    # p = pc.PointCloud(matrixofpoints_inR2)
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    p.ComputeDistanceMatrix()
    # Create Selector
    pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
    R = float(pointcloud_sel.getdistance_subsetstoPointcloud()) / 2
    # R = 0
    print 'R = ', R
    numdivision = 5
    maxdim = 3
    # ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision, maxdimension=maxdim)
    ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                           maxdimension=maxdim)
    ws.construct()
    ci = IntervalComputation(ws)
    ci.compute_intervals(
        maxdim)  # I should check everything is ok in this function since the deg for simplices can have real value now.
    ci.print_BettiNumbers()

if __name__ == "__main__":
    # testpointcloud()
    # testMatlabPointcloud()
    # testRandomSelector()
    # testRandomSelectorDistanceMetricio()
    # testMaxdist()
    testWitnessStream()
    # testWitnessStreamPH()
