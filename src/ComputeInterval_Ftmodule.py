__author__ = 'Naheed'

from src.ReductionAlgorithm import StandardMatrix
from src.Filtration import Filtration
from src.boundaryoperator import Boundary
from copy import deepcopy


class PintervaloverField:
    def __init__(self, K=1):
        '''
        K = P-interval upto K dimension
        '''
        self.maxdim = K
        self.betti_intervals = {}

    def ComputeIntervals(self, fil):

        for dim in xrange(1, self.maxdim + 2, 2):

            Mk = StandardMatrix(fil, dim)
            Mk_plusone = StandardMatrix(fil, dim + 1)
            mkhat, mkplusonehat = Mk.get_reduced_matrices(Mk_plusone.get_transpose())

            print 'printing reduced matrices'
            if mkhat:
                print 'mk hat:'
                for p in mkhat:
                    print str(p)
            else:
                print 'm', dim, " is Empty"

            print 'mk+1 hat:'
            if mkplusonehat:
                for p in mkplusonehat:
                    print str(p)
            else:
                print 'm', dim + 1, " is Empty"

            print Mk.interval
