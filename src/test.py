import numpy as np
import PointCloud as pc
import Selector as sel
from time import time
from guppy import hpy

def testpointcloud():
    matrixofpoints_inR2 = []
    mean = [0, 0]
    cov = [[1, 0], [0, 1]]
    matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    p = pc.PointCloud(matrixofpoints_inR2)
    print p.size, p.dimension
    p.compute_distancematrix()
    print p.distmat


def testMatlabPointcloud():
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    print p.dimension, p.size
    # p.compute_distancematrix()
    # print p.distmat

    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/pointsRange.mat'
    p = pc.MatlabPointCloud(filename, 'pointsRange')
    print p.dimension, p.size

def testTextPointCloud():
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/pointcloud.txt'
    p = pc.TextPointCloud(filename, ' ')
    print p.dimension, p.size
    p.compute_distancematrix()
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
    print s.getLandmarkPoints().points

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
    p.compute_distancematrix()
    # Create Selector
    pointcloud_sel = sel.PointCloudSelector(p, 100, "RandomSelector")
    R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud()) / 2
    # R = 0
    print 'R = ', R
    numdivision = 5
    maxdim = 3
    # ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision, maxdimension=maxdim)
    ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                           maxdimension=maxdim)

    ws.construct
    print ws
    print "Total number of Simplices in the Filtration: ", len(ws)


def testWitnessStreamPH():
    from WitnessFiltration import WitnessStream
    from src.WeakWitnessFiltration import WeakWitnessStream
    from src.ComputeInterval import IntervalComputation

    # mean = [0, 0]
    # cov = [[1, 0], [0, 1]]
    # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    # p = pc.PointCloud(matrixofpoints_inR2)
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    p.compute_distancematrix()
    # Create Selector
    # pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
    pointcloud_sel = sel.PointCloudSelector(p, 100, "MaxminSelector")

    # Measuring system time elapsed since the epoch (UTC time-zone)
    start_time = time()
    pointcloud_sel.select()
    elapsed_time = time() - start_time

    R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())
    # R = 0
    print 'R = ', R
    numdivision = 10
    maxdim = 2
    # ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision, maxdimension=maxdim)
    ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                           maxdimension=maxdim)
    ws.construct()
    print "Total number of Simplices in the Filtration: ", len(ws)
    ci = IntervalComputation(ws)
    ci.compute_intervals(
        maxdim)  # I should check everything is ok in this function since the deg for simplices can have real value now.
    ci.print_BettiNumbers()


def testWitnessStreamPerCom():
    from WitnessFiltration import WitnessStream
    from src.WeakWitnessFiltration import WeakWitnessStream
    from src.AbsoluteCohomologyOptimized import *
    from src.ComputeInterval import IntervalComputation

    # mean = [0, 0]
    # cov = [[1, 0], [0, 1]]
    # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
    # p = pc.PointCloud(matrixofpoints_inR2)
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    h = hpy() # guppy heap object
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    p.compute_distancematrix()
    # Create Selector
    # pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
    pointcloud_sel = sel.PointCloudSelector(p, 500, "MaxminSelector")

    # Measuring system time elapsed since the epoch (UTC time-zone)
    start_time = time()
    pointcloud_sel.select()
    elapsed_time = time() - start_time

    R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())
    # R = 0
    print 'R = ', R
    numdivision = 10
    maxdim = 2
    # ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision, maxdimension=maxdim)
    ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                           maxdimension=maxdim)
    ws.construct()
    print "Total number of Simplices in the Filtration: ", len(ws)

    print "After ws.construct():\n",h.heap().size

    start_time = time()
    cohom = FiltrationArrayCohomologyComputer(filtr=ws,
                                              maxdim=maxdim,maxfilter=R)
    total_mem_consumed = h.heap().size
    cohom.compute()
    total_mem_consumed = h.heap().size - total_mem_consumed
    elapsed_time = time() - start_time
    print "time: ", elapsed_time
    print "After cohomology:\n",total_mem_consumed

    start_time = time()
    ci = IntervalComputation(ws)
    total_mem_consumed = h.heap().size
    ci.compute_intervals(
        maxdim)  # I should check everything is ok in this function since the deg for simplices can have real value now.
    total_mem_consumed = h.heap().size - total_mem_consumed
    ci.print_BettiNumbers()
    elapsed_time = time() - start_time
    print "time: ", elapsed_time
    print "After Homology:\n", total_mem_consumed


def testRipsstream():
    # maxdim = 2
    # filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/pointcloud.txt'
    # p = pc.TextPointCloud(filename, ' ')
    maxdim = 2
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename,'point_cloud')
    print p.dimension, p.size
    p.compute_distancematrix()
    print p.getdistance(0,1)
    from src.RipsFiltration import BruteForceRips

    rf = BruteForceRips(p, 100, maxdim, 0.5)
    rf.construct()
    # print rf.write_boundarylists_to('/Users/naheed/PycharmProjects/PersistenceHomology/data/pointcloud.txt.fil')
    print len(rf)
    from src.ComputeInterval import IntervalComputation
    ci = IntervalComputation(rf)
    ci.compute_intervals(maxdim)
    ci.print_BettiNumbers()

if __name__ == "__main__":
    # testpointcloud()
    # testTextPointCloud()
    testRipsstream()
    # testMatlabPointcloud()
    # testRandomSelector()
    # testRandomSelectorDistanceMetricio()
    # testMaxdist()
    # testWitnessStream()
    # testWitnessStreamPH()
    # testWitnessStreamPerCom()
