from simplex import KSimplex
from boundaryoperator import Boundary

__author__ = 'Naheed'

INF = float('inf')


class IntervalComputation:
    def __init__(self, filtr):
        self.filtration_ar = []
        self.simplex_to_indexmap = {}
        self.betti_intervals = None

        maxk = -1
        for fil in filtr.listof_iFiltration.values():
            if fil.simplicial_complex.maxK > maxk:
                maxk = fil.simplicial_complex.maxK

        self.maxdim = maxk
        cnt = 0
        for k in range(maxk + 1):
            for i in range(len(filtr.listof_iFiltration)):
                for ksimplex in filtr.get_ksimplices_from_ithFiltration(k, i):
                    if ksimplex:
                        self.simplex_to_indexmap[tuple(ksimplex.kvertices)] = cnt
                        cnt += 1
                        self.filtration_ar.append(ksimplex)

        print [str(x) for x in self.filtration_ar]

        self.T = [None] * len(self.filtration_ar)
        self.marked = [False] * len(self.filtration_ar)
        self.j_ar = [None] * len(self.filtration_ar)

        print self.simplex_to_indexmap

    def compute_intervals(self, K):
        self.betti_intervals = [[] for i in range(K)]

        for j, sigmaj in enumerate(self.filtration_ar):
            d = self.remove_pivot_rows(sigmaj)
            print d
            if len(d) == 0:
                self.marked[j] = True
            else:
                i, i_ind = self.get_maxindexd(d)
                k = self.filtration_ar[i].k
                self.j_ar[i] = j
                # print '+'.join([str(sigma) for sigma in d])
                self.T[i] = d
                self.betti_intervals[k].append((self.filtration_ar[i].degree, sigmaj.degree))

        for j, sigmaj in enumerate(self.filtration_ar):
            if self.marked[j] and self.j_ar[j] is None:
                k = sigmaj.k
                self.betti_intervals[k].append((sigmaj.degree, INF))

    def remove_pivot_rows(self, sigma):
        assert isinstance(sigma, KSimplex)
        k = sigma.k
        bd = Boundary()
        d = set([])

        for sign, sigma in bd.compute_boundary(sigma):
            if self.marked[self.simplex_to_indexmap[tuple(sigma.kvertices)]]:
                d.add(tuple(sigma.kvertices))

        while 1:
            if len(d) == 0:
                break
            max_indexd, maxi_d = self.get_maxindexd(d)
            if self.j_ar[max_indexd] is None:
                break
            # Gaussian elimination here
            d.symmetric_difference_update(self.T[max_indexd])

        return d

    def get_maxindexd(self, set_ofsimplex_d):

        max_indexd = -1
        maxi = -1
        for i, sigma_bd in enumerate(set_ofsimplex_d):
            print sigma_bd
            cur_maxd = self.simplex_to_indexmap[sigma_bd]
            if cur_maxd > max_indexd:
                max_indexd = cur_maxd
                maxi = i
        return max_indexd, maxi
