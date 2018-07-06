from memory_profiler import profile
from idmanager import getId
from simplex import KSimplex
from Filtration import *
from boundaryoperator import Boundary

__author__ = 'Naheed'

INF = float('inf')


class IntervalComputation:
    """
    This class provides simple way of computing persistence which is compliant with the new Filtration definition.
    Simpler than ComputeInterval.py file
    """
    def __init__(self, filtr, maxk, max_filtration_val):
        assert isinstance(filtr, RealvaluedFiltration)

        self.maxdim = maxk
        self.maxfilter = max_filtration_val

        self.filtration_ar = []
        # # if dimensions are the same, ordered by their appearence time.
        self.simplex_to_indexmap = {}  # for simplex sigma it holds its index in filtration_ar[]
        self.betti_intervals = [[] for _ in xrange(self.maxdim + 1)]
        self.representative_cycles = [[] for _ in xrange(self.maxdim + 1)]

        cnt = 0
        for simplex in filtr.get_simplices():
            if simplex.k < self.maxdim + 1:
                self.filtration_ar.append(simplex)
                self.simplex_to_indexmap[simplex.id] = cnt
                cnt += 1
            if simplex.degree > self.maxfilter: # We were traversing the simplices in ascending order of filtration val.
                break

        self.T = [None] * cnt
        self.marked = [False] * cnt  # Boolean flag for marked simplices.
        self.j_ar = [None] * cnt
        self.num_active_simplices = cnt  # Number of simplices which are actually being used in persistence computation.

    # @profile
    def compute_intervals(self):
        """
        :param K: K as in Betti_K
        :return: Betti_0,Betti_1,...,upto Betti_K intervals
        """
        for j, sigmaj in enumerate(self.filtration_ar):
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
                    self.betti_intervals[k].append((self.filtration_ar[i].getdegree(), sigmaj.getdegree()))

        for j, sigmaj in enumerate(self.filtration_ar):
            if self.marked[j] and self.j_ar[j] is None:
                k = sigmaj.k
                self.betti_intervals[k].append((sigmaj.getdegree(),INF))

    def remove_pivot_rows(self, simplex):
        # assert isinstance(simplex, KSimplex)
        k = simplex.k
        bd = Boundary()
        d = set([])
        z = []  # the basis formed by repeated addition

        for sigma in bd.compute_boundary(simplex):
            if self.marked[self.simplex_to_indexmap[sigma]]:
                d.add(sigma)

        z.append(simplex)
        while 1:
            if len(d) == 0:
                break

            max_indexd, _ = self.get_maxindexd(d)
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

    def get_intervals_asnumpyarray(self):
        """
        Returns the persistent intervals as numpy array of size nx3
        :returns numpy array
        """
        import numpy as np
        total_bars = 0
        for l in self.betti_intervals:
            total_bars += len(l)

        # dt = np.dtype([('dim', int), ('birth',float), ('death',float)])
        # dt = np.dtype({'names': ['dim', 'birth', 'death'], 'formats': ['i8', 'f8', 'f8']})
        out = np.empty((0,3))

        for dim, l in enumerate(self.betti_intervals):
            for tup in l:
                out = np.append(out, np.asarray([dim, tup[0], tup[1]]))

        return out.reshape((total_bars, 3))


# class IntervalComputation_heapset:
#     """
#     This class provides simple way of computing persistence.  Simpler than ComputeInterval.py file
#     """
#     def __init__(self, filtr, maxk):
#         assert isinstance(filtr, RealvaluedFiltration)
#
#         self.maxdim = min(filtr.maxfiltration_val, maxk)
#
#         self.filtration_ar = []
#         # # if dimensions are the same, ordered by their appearence time.
#         self.simplex_to_indexmap = {}  # for simplex sigma it holds its index in filtration_ar[]
#         self.betti_intervals = [[] for _ in xrange(self.maxdim + 1)]
#         self.representative_cycles = [[] for _ in xrange(self.maxdim + 1)]
#
#         cnt = 0
#         for simplex in filtr.get_simplices():
#             if simplex.k <= self.maxdim + 1:
#                 self.filtration_ar.append(simplex)
#                 self.simplex_to_indexmap[tuple(simplex.kvertices)] = cnt
#                 cnt += 1
#
#         self.T = [None] * len(filtr.totalsimplices)
#         self.marked = [False] * len(filtr.totalsimplices)  # Boolean flag for marked simplices.
#         self.j_ar = [None] * len(filtr.totalsimplices)
#
#     # @profile
#     def compute_intervals(self):
#         """
#         :param K: K as in Betti_K
#         :return: Betti_0,Betti_1,...,upto Betti_K intervals
#         """
#         for j, sigmaj in enumerate(self.filtration_ar):
#             d = self.remove_pivot_rows(sigmaj)
#             #print d
#             if len(d) == 0:
#                 self.marked[j] = True
#             else:
#                 i, i_ind = self.get_maxindexd(d)
#                 k = self.filtration_ar[i].k  # dimension of sigmai (according to paper)
#                 self.j_ar[i] = j
#                 # print '+'.join([str(sigma) for sigma in d])
#                 self.T[i] = d
#                 if self.filtration_ar[i].degree <= sigmaj.degree:
#                     self.betti_intervals[k].append((self.filtration_ar[i].getdegree(), sigmaj.getdegree()))
#
#         for j, sigmaj in enumerate(self.filtration_ar):
#             if self.marked[j] and self.j_ar[j] is None:
#                 k = sigmaj.k
#                 self.betti_intervals[k].append((sigmaj.getdegree(),INF))
#
#     def remove_pivot_rows(self, simplex):
#         # assert isinstance(simplex, KSimplex)
#         k = simplex.k
#         bd = Boundary()
#         d = set([])
#         z = []  # the basis formed by repeated addition
#
#         for sign, sigma in bd.compute_boundary(simplex):
#             if self.marked[self.simplex_to_indexmap[tuple(sigma.kvertices)]]:
#                 d.add(tuple(sigma.kvertices))
#
#         z.append(simplex)
#         while 1:
#             if len(d) == 0:
#                 break
#
#             max_indexd, maxi_d = self.get_maxindexd(d)
#             if self.j_ar[max_indexd] is None:
#                 break
#             z.append(self.filtration_ar[self.j_ar[max_indexd]])
#             # Gaussian elimination here
#             d.symmetric_difference_update(self.T[max_indexd])
#
#         if len(d) == 0:
#             k = simplex.k
#             if k < len(self.representative_cycles):
#                 self.representative_cycles[k].append(z)
#
#         return d
#
#     def get_maxindexd(self, set_ofsimplex_d):
#
#         max_indexd = -1
#         maxi = -1
#         for i, sigma_bd in enumerate(set_ofsimplex_d):
#             #print sigma_bd
#             cur_maxd = self.simplex_to_indexmap[sigma_bd]
#             if cur_maxd > max_indexd:
#                 max_indexd = cur_maxd
#                 maxi = i
#         return max_indexd, maxi
#
#     def print_BettiNumbers(self):
#         repr = ''
#         for dim, li in enumerate(self.betti_intervals):
#             repr += ('dim: ' + str(dim) + '\n')
#             for tup in li:
#                 if tup[0] == tup[1]:
#                     continue
#                 repr += str(tup)
#             repr += '\n'
#         print repr
#
#     def get_representativs(self):
#         """
#         :return: Returns Representative Holes (BUGGY CODE)
#         """
#         repr = ''
#         for idx, whatever in enumerate(self.representative_cycles):
#             if whatever:
#                 repr += "id: " + str(idx) + '{'
#                 for w in whatever:
#                     repr += "+".join([str(i) for i in w])
#                     repr += " "
#                 repr += "}\n"
#                 # repr+="\n"
#         print repr
#
#     def get_intervals_asnumpyarray(self):
#         """
#         Returns the persistent intervals as numpy array of size nx3
#         :returns numpy array
#         """
#         import numpy as np
#         total_bars = 0
#         for l in self.betti_intervals:
#             total_bars += len(l)
#
#         # dt = np.dtype([('dim', int), ('birth',float), ('death',float)])
#         # dt = np.dtype({'names': ['dim', 'birth', 'death'], 'formats': ['i8', 'f8', 'f8']})
#         out = np.empty((0,3))
#
#         for dim, l in enumerate(self.betti_intervals):
#             for tup in l:
#                 out = np.append(out, np.asarray([dim, tup[0], tup[1]]))
#
#         return out.reshape((total_bars, 3))