__author__ = 'Naheed'

import numpy as np
import PointCloud as Pc
from Selector import GraphSelector
from time import time
# from guppy import hpy
from memory_profiler import memory_usage, profile
import networkx as nx
from WitnessFiltration import WitnessStream
from WeakWitnessFiltration import WeakWitnessStream
from ComputePersistence import *
from src.IncrementalRips import IncrementalRips
from src.utils import comparePIntervals

def testgraphrips():
    # path = '/Users/naheed/Google Drive/tda-sna/'
    # filename = 'core-blah.txt'
    # path = '/Users/naheed/Google Drive/tda-sna/animal/'
    # filename = 'dolphin.txt'
    # g = nx.read_edgelist(path + filename, nodetype=int, data=(('weight', float),))

    path = '/Users/naheed/Google Drive/tda-sna/ppi/'
    filename = 'rat-inact-ppi.txt'
    g = nx.read_edgelist(path + filename, nodetype=str, data=(('weight', float),))

    maxdim = 1  # we want to compute upto maxdim-th homology. For that need to construct maxdim and maxdim+1 simplices.
    maxfilter = 0.3

    print 'graph size ', len(g.nodes)
    print 'number of edges = ', len(g.edges)

    p = Pc.GraphPointcloud(nxgraph=g)
    p.compute_distancematrix() # Compute all pair shortest path (normalized)
    print "max distance: ", p.maxdist

    rf = IncrementalRips(p, 10, maxdim, maxfilter)
    rf.construct()
    print 'filtration size ', len(rf)
    # print rf
    ci = IntervalComputation(rf, maxk=maxdim, max_filtration_val=maxfilter)
    ci.compute_intervals()
    ci.print_BettiNumbers()

if __name__ == "__main__":
    testgraphrips()

