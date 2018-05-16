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
    pointcloud_sel = sel.PointCloudSelector(p, 50, "MaxminSelector")

    # Measuring system time elapsed since the epoch (UTC time-zone)
    start_time = time()
    pointcloud_sel.select()
    elapsed_time = time() - start_time

    R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())/3
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

    rf = BruteForceRips(p, 100, maxdim, 0.02)
    rf.construct()
    print rf.write_boundarylists_to('/Users/naheed/PycharmProjects/PersistenceHomology/data/eight_mat.fil')
    print len(rf)
    from src.ComputeInterval import IntervalComputation
    ci = IntervalComputation(rf)
    ci.compute_intervals(maxdim)
    npar= ci.get_intervals_asnumpyarray()
    print npar[:10]
    print npar.shape
    import numpy as np

    with open("test.csv",'wb') as f:
        f.write("Dimension,Birth,Death\n")
        np.savetxt(f, npar, delimiter=",", fmt='%d,%.4f,%.4f')
    ci.print_BettiNumbers()

    from src.Intervalviz import PersistenceViz
    pv = PersistenceViz(ci.betti_intervals, replace_Inf=rf.maxfiltration_val)
    pv.draw_barcodes()

def comparebars():
    maxdim = 2
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p = pc.MatlabPointCloud(filename, 'point_cloud')
    print p.dimension, p.size
    p.compute_distancematrix()
    print p.getdistance(0, 1)
    from src.RipsFiltration import BruteForceRips
    rf = BruteForceRips(p, 100, maxdim, 0.01)
    rf.construct()
    from src.ComputeInterval import IntervalComputation
    ci = IntervalComputation(rf)
    ci.compute_intervals(maxdim)
    print ci.betti_intervals

    from src.WeakWitnessFiltration import WeakWitnessStream
    filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
    p2 = pc.MatlabPointCloud(filename, 'point_cloud')
    print p2.dimension, p2.size
    p2.compute_distancematrix()
    pointcloud_sel = sel.PointCloudSelector(p2, 200, "MaxminSelector")
    pointcloud_sel.select()
    R = 0.01
    print "R= ",R
    ws = WeakWitnessStream(mu=1, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=100,
                           maxdimension=maxdim)

    ws.construct()
    ci2 = IntervalComputation(ws)
    ci2.compute_intervals(maxdim)

    # print len(ci2.betti_intervals), len(ci.betti_intervals)

    from src.Intervalviz import PersistenceViz
    pv = PersistenceViz(ci.betti_intervals, replace_Inf=rf.maxfiltration_val)
    pv.qual_compare_barcodes(ci2.betti_intervals, R)

def testCSVreader():
    from src.Intervalviz import PersistenceViz
    # root= "/Users/naheed/Google Drive/tda-sna/animal/"
    # pInterval_files = [root+"dolphin_normalized_0.csv", root+"dolphin_normalized_1.csv", root+"dolphin_normalized_2.csv"]
    # pv = PersistenceViz.input_int_fromCSVs(pInterval_files)
    # pv.draw_barcodes()

    prefix = "/Users/naheed/Google Drive/tda-sna/Results/lazy250/WS_500_5/lazywit_landscap100/"
    prob = [0.0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8, 0.9, 1.0]
    root = [ (prefix+ "lw100_500_5_"+ str(i)+ ".edges_normalized") for i in prob]

    prefix2 = "/Users/naheed/Google Drive/tda-sna/Results/lazy250/WS_500_5/"
    root2 = [ (prefix2 + "500_5_"+ str(i)+ ".edges_normalized") for i in prob]

    for  i, (root,root2) in enumerate(zip(root,root2)):
        pInterval_files = [root + "_0.csv.csv", root + "_1.csv.csv", root + "_2.csv.csv"]
        pv = PersistenceViz.input_int_threecolumned_fromCSVs(pInterval_files, replace_inf=1.0)
        # pv.draw_barcodes()


        pInterval_files2 = [root2+"_0.csv", root2+"_1.csv", root2+"_2.csv"]
        pv2 = PersistenceViz.input_int_fromCSVs(pInterval_files2, replace_inf=1.0)
        # pv2.draw_barcodes()
        param={"title":"Probability = "+str(prob[i]), "xlabels": ("Weak-Witness", "Vietoris Rips")}
        pv.qual_compare_barcodes_fromPersViz(secondbarViz= pv2, write=True,writefilename="WScompare_500_5_"+ str(prob[i])+ ".pdf", param = param)

if __name__ == "__main__":
    # testpointcloud()
    # testTextPointCloud()
    # testRipsstream()
    # testMatlabPointcloud()
    # testRandomSelector()
    # testRandomSelectorDistanceMetricio()
    # testMaxdist()
    # testWitnessStream()
    # testWitnessStreamPH()
    # testWitnessStreamPerCom()

    # comparebars()
    testCSVreader()