from __future__ import division
import numpy as np

__author__ = 'Naheed'


def testWitnessStream_Maxmin(Numberoftimesrun=100):
    from time import time
    from src.WitnessFiltration import WitnessStream
    from src.WeakWitnessFiltration import WeakWitnessStream
    import src.Selector as sel
    import src.PointCloud as pc

    selector_execution_times = [0.0] * Numberoftimesrun
    filtration_execution_times = [0.0] * Numberoftimesrun
    strong_filtration_exectimes = [0.0] * Numberoftimesrun

    for n in xrange(Numberoftimesrun):
        print "Iteration: ", n
        # mean = [0, 0]
        # cov = [[1, 0], [0, 1]]
        # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
        # p = pc.PointCloud(matrixofpoints_inR2)
        filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
        p = pc.MatlabPointCloud(filename, 'point_cloud')
        p.compute_distancematrix()

        NumLandmarks = int(
            p.size / 50)  # Typically for 2D, according to paper <= N/20. so N/20, N/25, N/30, N/35, N/40 is fine
        print "#Landmark: ", NumLandmarks
        # Create Selector
        # pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
        pointcloud_sel = sel.PointCloudSelector(p, NumLandmarks, "MaxminSelector")
        # Measuring system time elapsed since the epoch (UTC time-zone)
        start_time = time()
        pointcloud_sel.select()
        elapsed_time = time() - start_time
        selector_execution_times[n] = elapsed_time

        R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())
        # R = 0
        print 'R = ', R
        numdivision = 10
        maxdim = 2

        # Run Lazy Witness stream
        ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                               maxdimension=maxdim)
        start_time = time()
        ws.construct()
        elapsed_time = time() - start_time
        filtration_execution_times[n] = elapsed_time

        # Run Strong Witness Stream
        strong_ws = WitnessStream(landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                                  maxdimension=maxdim)
        start_time = time()
        strong_ws.construct()
        elapsed_time = time() - start_time
        strong_filtration_exectimes[n] = elapsed_time

    selector_execution_times = np.array(selector_execution_times)
    filtration_execution_times = np.array(filtration_execution_times)
    strong_filtration_exectimes = np.array(strong_filtration_exectimes)

    print "Mean (,", Numberoftimesrun, " run) runtime for Maxmin selection: \n", np.mean(selector_execution_times)
    print "Standard deviation (", Numberoftimesrun, " run) runtime for Maxmin selection: \n", np.std(
        selector_execution_times)

    print "Mean (", Numberoftimesrun, " run) runtime for Lazy Witness: \n", np.mean(filtration_execution_times)
    print "Standard deviation (", Numberoftimesrun, " run) runtime for Lazy Witness: \n", np.std(
        filtration_execution_times)

    print "Mean (", Numberoftimesrun, " run) runtime for Strong Witness: \n", np.mean(strong_filtration_exectimes)
    print "Standard deviation (", Numberoftimesrun, " run) runtime for Strong Witness: \n", np.std(
        strong_filtration_exectimes)


def generate(N, D, rootdir):
    from time import time
    from src.WeakWitnessFiltration import WeakWitnessStream
    import src.Selector as sel
    import src.PointCloud as pc

    filtration_sizes = [0.0] * N

    for n in xrange(N):
        # print "Iteration: ", n
        # mean = [0, 0]
        # cov = [[1, 0], [0, 1]]
        # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
        # p = pc.PointCloud(matrixofpoints_inR2)
        filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/eight.mat'
        p = pc.MatlabPointCloud(filename, 'point_cloud')
        p.compute_distancematrix()

        # Typically for 2D, according to paper <= N/20. so N/20, N/25, N/30, N/35, N/40 is fine
        NumLandmarks = int(p.size / D)
        # print "#Landmark: ", NumLandmarks

        # Create Selector
        # pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
        pointcloud_sel = sel.PointCloudSelector(p, NumLandmarks, "MaxminSelector")
        # Select point
        pointcloud_sel.select()

        R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())
        # R = 0
        # print 'R = ', R
        numdivision = 20
        maxdim = 2

        # Run Lazy Witness stream
        ws = WeakWitnessStream(mu=2, landmarkselector=pointcloud_sel, maxdistance=R, numdivision=numdivision,
                               maxdimension=maxdim)
        ws.construct()

        filtration_sizes[n] = len(ws)

        ws.write_boundarylists_to(rootdir+'eight'+'_'+str(maxdim)+'_'+str(NumLandmarks)+"_"+str(len(ws))+".fil")
        # start_time = time()
        # cohom = FiltrationArrayCohomologyComputer(ws, maxdim, R)
        # cohom.compute()
        # abs_cohom_exectime[n] = time() - start_time
        #
        # start_time = time()
        # ci = IntervalComputation(ws)
        # ci.compute_intervals(maxdim)  # I should
        # abs_hom_exectime[n] = time() - start_time
        #
        # if cohom.compare(ci.betti_intervals):
        #     print 'equal'
        # else:
        #     print 'not equal'

    # abs_hom_exectime = np.array(abs_hom_exectime)
    # abs_cohom_exectime = np.array(abs_cohom_exectime)

    print "Average number of simplices in the filtration: \n", np.mean(filtration_sizes)

    # print "Mean (,", N, " run) runtime for Absolute Homology: \n", np.mean(abs_hom_exectime)
    # print "Standard deviation (", N, " run) runtime for Absolute Homology: \n", np.std(
    #     abs_hom_exectime)
    #
    # print "Mean (,", N, " run) runtime for Absolute Cohomology: \n", np.mean(abs_cohom_exectime)
    # print "Standard deviation (", N, " run) runtime for Absolute Cohomology: \n", np.std(
    #     abs_cohom_exectime)

def generateForNaturalImg(N, D, rootdir):
    from time import time
    from src.WeakWitnessFiltration import WeakWitnessStream
    import src.Selector as sel
    import src.PointCloud as pc

    filtration_sizes = [0.0] * N

    for n in xrange(N):
        # print "Iteration: ", n
        # mean = [0, 0]
        # cov = [[1, 0], [0, 1]]
        # matrixofpoints_inR2 = np.random.multivariate_normal(mean, cov, 100)
        # p = pc.PointCloud(matrixofpoints_inR2)
        filename = '/Users/naheed/PycharmProjects/PersistenceHomology/data/pointsRange.mat'
        p = pc.MatlabPointCloud(filename, 'pointsRange')
        p.compute_distancematrix()

        # Typically for 2D, according to paper <= N/20. so N/20, N/25, N/30, N/35, N/40 is fine
        NumLandmarks = int(p.size / D)
        # print "#Landmark: ", NumLandmarks

        # Create Selector
        # pointcloud_sel = sel.PointCloudSelector(p, 10, "RandomSelector")
        pointcloud_sel = sel.PointCloudSelector(p, NumLandmarks, "MaxminSelector")
        # Select point
        pointcloud_sel.select()

        R = float(pointcloud_sel.get_maxdistance_landmarktoPointcloud())
        # R = 0
        # print 'R = ', R
        numdivision = 1000
        maxdim = 3

        # Run Lazy Witness stream
        ws = WeakWitnessStream(mu=1, landmarkselector=pointcloud_sel, maxdistance=R/3, numdivision=numdivision,
                               maxdimension=maxdim)
        ws.construct()

        filtration_sizes[n] = len(ws)

        ws.write_boundarylists_to(rootdir+'eight'+'_'+str(maxdim)+'_'+str(NumLandmarks)+"_"+str(len(ws))+".fil")
        # start_time = time()
        # cohom = FiltrationArrayCohomologyComputer(ws, maxdim, R)
        # cohom.compute()
        # abs_cohom_exectime[n] = time() - start_time
        #
        # start_time = time()
        # ci = IntervalComputation(ws)
        # ci.compute_intervals(maxdim)  # I should
        # abs_hom_exectime[n] = time() - start_time
        #
        # if cohom.compare(ci.betti_intervals):
        #     print 'equal'
        # else:
        #     print 'not equal'

    # abs_hom_exectime = np.array(abs_hom_exectime)
    # abs_cohom_exectime = np.array(abs_cohom_exectime)

    print "Average number of simplices in the filtration: \n", np.mean(filtration_sizes)

    # print "Mean (,", N, " run) runtime for Absolute Homology: \n", np.mean(abs_hom_exectime)
    # print "Standard deviation (", N, " run) runtime for Absolute Homology: \n", np.std(
    #     abs_hom_exectime)
    #
    # print "Mean (,", N, " run) runtime for Absolute Cohomology: \n", np.mean(abs_cohom_exectime)
    # print "Standard deviation (", N, " run) runtime for Absolute Cohomology: \n", np.std(
    #     abs_cohom_exectime)



if __name__ == "__main__":
    # Test Average execution time of Eight data, time to sample 100 landmarks in Maxmin and Constrution of filtration
    # For strong, Lazy both
    # testWitnessStream_Maxmin(100)
    for d in range(10, 5-1, -1):
        print "d: ", d
        generateForNaturalImg(1, d,rootdir='/Users/naheed/PycharmProjects/PersistenceHomology/data/')
