from simplex import KSimplex
from boundaryoperator import Boundary

__author__ = 'Naheed'

INF = float('inf')


class IntervalComputation:
    def __init__(self, filtr):
        self.filtration_ar = []  # Holds the ordered list of simplices accros the filtration. simplices of dimension k appears before k+1.
        # # if dimensions are the same, ordered by their appearence time.
        self.simplex_to_indexmap = {}  # for simplex sigma it holds its index in filtration_ar[]
        self.betti_intervals = None
        self.representative_cycles = []

        maxk = -1
        for fil in filtr.listof_iFiltration.values():
            if fil.simplicial_complex.maxK > maxk:
                maxk = fil.simplicial_complex.maxK

        self.maxdim = maxk
        cnt = 0
        for k in xrange(maxk + 1):
            for i in filtr.listof_iFiltration.keys():
                for ksimplex in filtr.get_ksimplices_from_ithFiltration(k, i):
                    if ksimplex:
                        self.simplex_to_indexmap[tuple(ksimplex.kvertices)] = cnt
                        cnt += 1
                        self.filtration_ar.append(ksimplex)

        # print [str(x) for x in self.filtration_ar]

        self.T = [None] * len(self.filtration_ar)
        self.marked = [False] * len(self.filtration_ar)  # Boolean flag for marked simplices.
        self.j_ar = [None] * len(self.filtration_ar)

        #print self.simplex_to_indexmap

    def compute_intervals(self, K=None):
        """
        :param K: K as in Betti_K
        :return: Betti_0,Betti_1,...,upto Betti_K intervals
        """
        if K:
            self.betti_intervals = [[] for i in xrange(K + 1)]
            self.representative_cycles = [[] for i in xrange(K + 1)]
        else:
            self.betti_intervals = [[] for i in xrange(self.maxdim + 1)]
            self.representative_cycles = [[] for i in xrange(self.maxdim + 1)]

        for j, sigmaj in enumerate(self.filtration_ar):
            if K:
                if sigmaj.k > K + 1:  # We only want  dimension upto K, i.e birth-death of 0,1,...,upto K simplices.
                    break  # K-simplices occur as boundary of K+1 simplices. therefore we need sigmaj.k <= K+1
            d = self.remove_pivot_rows(sigmaj)
            #print d
            if len(d) == 0:
                self.marked[j] = True
            else:
                i, i_ind = self.get_maxindexd(d)
                k = self.filtration_ar[i].k  # dimension of sigmai (according to paper)
                self.j_ar[i] = j
                # print '+'.join([str(sigma) for sigma in d])
                self.T[i] = d
                if self.filtration_ar[i].degree <= sigmaj.degree:
                    self.betti_intervals[k].append((self.filtration_ar[i].degree, sigmaj.degree))

        for j, sigmaj in enumerate(self.filtration_ar):
            if K:
                if sigmaj.k > K:  # We only want  dimension upto K, i.e birth-death of 0,1,...,upto K simplices.
                    break  # K-simplices occur as boundary of K+1 simplices. therefore we need sigmaj.k <= K+1
            if self.marked[j] and self.j_ar[j] is None:
                k = sigmaj.k
                self.betti_intervals[k].append((sigmaj.degree, INF))

    def remove_pivot_rows(self, simplex):
        assert isinstance(simplex, KSimplex)
        k = simplex.k
        bd = Boundary()
        d = set([])
        z = []  # the basis formed by repeated addition

        for sign, sigma in bd.compute_boundary(simplex):
            if self.marked[self.simplex_to_indexmap[tuple(sigma.kvertices)]]:
                d.add(tuple(sigma.kvertices))

        z.append(simplex)
        while 1:
            if len(d) == 0:
                break

            max_indexd, maxi_d = self.get_maxindexd(d)
            if self.j_ar[max_indexd] is None:
                break
            z.append(self.filtration_ar[self.j_ar[max_indexd]])
            # Gaussian elimination here
            d.symmetric_difference_update(self.T[max_indexd])

        if len(d) == 0:
            k = simplex.k
            if k < len(self.representative_cycles):
                self.representative_cycles[k].append(z)

        return d

    def get_maxindexd(self, set_ofsimplex_d):

        max_indexd = -1
        maxi = -1
        for i, sigma_bd in enumerate(set_ofsimplex_d):
            #print sigma_bd
            cur_maxd = self.simplex_to_indexmap[sigma_bd]
            if cur_maxd > max_indexd:
                max_indexd = cur_maxd
                maxi = i
        return max_indexd, maxi

    def print_BettiNumbers(self):
        repr = ''
        for dim, li in enumerate(self.betti_intervals):
            repr += ('dim: ' + str(dim) + '\n')
            for tup in li:
                if tup[0] == tup[1]:
                    continue
                repr += str(tup)
            repr += '\n'
        print repr

    def get_representativs(self):
        """
        :return: Returns Representative Holes (BUGGY CODE)
        """
        repr = ''
        for idx, whatever in enumerate(self.representative_cycles):
            if whatever:
                repr += "id: " + str(idx) + '{'
                for w in whatever:
                    repr += "+".join([str(i) for i in w])
                    repr += " "
                repr += "}\n"
                # repr+="\n"
        print repr
