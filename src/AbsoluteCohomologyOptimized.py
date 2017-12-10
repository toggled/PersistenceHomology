"""
pCoh algorithm as described in paper (not so elaborately though):- DUALITIES IN PERSISTENT (CO)HOMOLOGY.
and explained elaborately in:- Persistent Cohomology and Circular Coordinates
"""
__author__ = 'Naheed'

from collections import Set
from src.simplex import KSimplex
from src.boundaryoperator import Boundary
from idmanager import getId

INF = float('inf')


# We implement this function as a generator for Persistent Intervals. Sweet!
# def cohomology_computer():
#     """
#     Given a new incoming simplex, this function decides whether to keep it in memory (A new cocycle is born)
#     or discard it (An old cocyle destroyed (also deleted from memory))
#     :rtype: tuple either (a,b) or (c,'inf')
#     """
#     indices = []  # I_0 = \phi
#     cocycles_sofar = []
#
#     def compute_persistent_cohomology(simplex):
#         assert isinstance(simplex, KSimplex)

# class NaiveCohomologyComputer(object):
#     def __init__(self, simplices, filtrations):
#         self.simplices = simplices  # Simplices are list here
#         self.filtrations = filtrations  # filtration list
#         self.intervals = []
#
#     def compute(self, maxdim=2, maxfilter=100.0):
#         # Implement maxdim, maxfilter optimization later perhaps.
#         first_simplex = KSimplex([self.simplices[0]], self.filtrations[0])
#         first_simplex.id = getId()
#         cc = compute_cohomology(first_simplex)
#         b, d = cc.next()
#         if b < d:
#             self.intervals.append((b, d))
#         index = 1
#         while index < len(self.simplices):
#             if self.filtrations[index] > maxfilter:
#                 break
#             if len(self.simplices[index]) - 1 > maxdim:
#                 break
#             simplextosend = KSimplex(self.simplices[index], degree=self.filtrations[index])
#             simplextosend.id = getId()
#             b, d = cc.send(simplextosend)
#             if b < d:
#                 self.intervals.append((b, d))
#             index = index + 1
#
#         while True:
#             b, d = cc.send(KSimplex([]))
#             if b < d:
#                 self.intervals.append((b, d))
#             if b == -1 or d == -1:
#                 break
#         cc.close()
#         return self.intervals


# class NaiveCohomologyComputer(object):
#     def __init__(self, filtration_obj):
#         self.filtrations = filtration_obj  # filtration list
#         self.intervals = []
#
#     def compute(self, maxdim=2, maxfilter=100.0):
#         first_simplex = KSimplex([self.simplices[0]], self.filtrations[0])
#         cc = compute_cohomology(first_simplex)
#         b, d = cc.next()
#         if b < d:
#             self.intervals.append((b, d))
#         index = 1
#         while index < len(self.simplices):
#             if self.filtrations[index] > maxfilter:
#                 break
#             if len(self.simplices[index]) - 1 > maxdim:
#                 break
#             simplextosend = KSimplex(self.simplices[index], degree=self.filtrations[index])
#             b, d = cc.send(simplextosend)
#             if b < d:
#                 self.intervals.append((b, d))
#             index = index + 1
#
#         while True:
#             b, d = cc.send(KSimplex([]))
#             if b < d:
#                 self.intervals.append((b, d))
#             if b == -1 or d == -1:
#                 break
#         cc.close()
#         return self.intervals


# old version
# class FiltrationArrayCohomologyComputer(NaiveCohomologyComputer):
#     def __init__(self, filtr, maxdim):
#         self.simplices = []
#         self.filtrations = []
#         for k in xrange(maxdim + 1):
#             for i in xrange(len(filtr.listof_iFiltration)):
#                 for ksimplex in filtr.get_ksimplices_from_ithFiltration(k, i):
#                     if ksimplex:
#                         self.simplices.append(ksimplex.kvertices)
#                         self.filtrations.append(ksimplex.degree)
#
#         super(FiltrationArrayCohomologyComputer, self).__init__(simplices=self.simplices, filtrations=self.filtrations)
#
#     def compute(self, maxdim, maxfilter):
#         return NaiveCohomologyComputer(self.simplices, self.filtrations).compute(maxdim=maxdim, maxfilter=maxfilter)


# def compute_cohomology(value=None):
#     """
#     Given a new incoming simplex, this function decides whether to keep it in memory (A new cocycle is born)
#     or discard it (An old cocyle destroyed (also deleted from memory))
#     :rtype: tuple either (a,b) or (c,'inf')
#     """
#     # print "Execution starts when 'next()' is called for the first time."
#     indices = []
#     id_to_degree_map = {}  # key = id, value = filtration appearence/degree
#     cardinalities = {}  # id vs cardinality map
#     # cocycles = {}  # key = id, value = cocycle. Each cocyle is implemented as a set. since we only care about Z_2.
#     # the whole simplex in the indices array.
#     assert isinstance(value, KSimplex)
#     try:
#         while True:
#             birth = death = value.degree  # since, we ignore such cases typically.
#
#             # Though theoretically its not the right thing to do.
#             try:
#                 if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
#                     if indices == []:
#                         birth = death = -1
#                     else:
#                         i = indices.pop(0)
#                         birth = id_to_degree_map[i]
#                         death = INF
#                         del id_to_degree_map[i]
#
#                 elif value.k == 0:  # For vertices
#                     indices.insert(0, value.id)
#                     cardinalities[value.id] = value.k + 1
#                     id_to_degree_map[value.id] = value.degree
#
# This elif part is buggy. coz the if line inside it is not gonna work.
#                 elif value.k > 0:
#                     flag_allzero = True
#                     id_to_del = -1
#                     index_to_del = -1
#                     for indx, id in enumerate(indices):
#                         if cardinalities[id] == (value.k):
#                             # boundary with last non zero pivot i.e in D^Transpose matrix. the left-most column in a row
#                             flag_allzero = False
#                             id_to_del = id
#                             index_to_del = indx
#                             break
#                             # Actually i should continue to update the later cycles's the basis. Will to that later.
#
#                     if not flag_allzero:
#                         # Delete
#                         indices.pop(index_to_del)  # removes the first occurance of this id
#                         birth = id_to_degree_map[id_to_del]
#                         death = value.degree
#                         del cardinalities[id_to_del]
#                         del id_to_degree_map[id_to_del]
#                     else:  # New cocycle. Keep it in indices.
#                         indices.insert(0, value.id)
#                         cardinalities[value.id] = value.k + 1
#                         id_to_degree_map[value.id] = value.degree
#
#                 value = (yield (birth, death))
#             except Exception, e:
#                 value = e
#     finally:
#         # print "Don't forget to clean up when 'close()' is called."
#         del indices
#         del cardinalities
#         del id_to_degree_map



class FiltrationArrayCohomologyComputer():
    """
    Given a filtration and its parameters, provides functionality to compute persistent cohomology
     using the algorithm pCoh as described in "Persistent Cohomology and Circular Coordinates" paper.
    """

    def __init__(self, filtr, maxdim, maxfilter):
        self.intervals = [[] for i in range(maxdim + 1)]
        first_simplex = KSimplex([])
        self.cc = compute_cohomology(first_simplex)
        b, d, dimension = self.cc.next()  # does nothing with this output. we are doing this cause we can not do send() successively unless we call .next() first

        self.maxdim = maxdim
        self.filtr = filtr
        self.maxdegree = maxfilter

    def compute(self):
        """
        Compute the persistent cohomology using
        """
        for k in xrange(self.maxdim + 1):
            for i in xrange(len(self.filtr.listof_iFiltration)):
                for ksimplex in self.filtr.get_ksimplices_from_ithFiltration(k, i):
                    if ksimplex and ksimplex.degree <= self.maxfilter:
                        b, d, dimension = self.cc.send(ksimplex)
                        if b < d:
                            self.intervals[dimension].append((b, d))
        while True:
            b, d, dimension = self.cc.send(KSimplex([], -1))
            if b < d:
                self.intervals[dimension].append((b, d))
            if b == -1 or d == -1:
                break
        self.cc.close()

        for i, listof in enumerate(self.intervals):
            print i
            print listof


# An optimized version of Persistent Cohomology algorithm. Only outputs birth-death pairs
def compute_cohomology(value=None):
    """
    Given a new incoming simplex, this function decides whether to keep it in memory (A new cocycle is born)
    or discard it (An old cocyle destroyed (also deleted from memory))
    :rtype: tuple either (a,b) or (c,'inf')
    """
    # print "Execution starts when 'next()' is called for the first time."
    # indices = []
    id_to_degree_map = {}  # key = id, value = filtration appearence/degree
    cardinalities = {}  # key = id, value = cardinality of the simplex identfied by id
    # cocycles = {}  # key = id, value = cocycle. Each cocyle is implemented as a set. since we only care about Z_2.
    # the whole simplex in the indices array.


    assert isinstance(value, KSimplex)
    try:
        while True:
            birth = death = value.degree  # since, we ignore such cases typically.
            dim = value.k
            # Though theoretically its not the right thing to do.
            try:
                if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
                    if id_to_degree_map.keys() == []:
                        birth = death = -1
                        value = (yield (birth, death, dim))
                    else:
                        # i = indices.pop(0)
                        # birth = id_to_degree_map[i]

                        # dim = cardinalities[i] - 1
                        # del id_to_degree_map[i]
                        for i in id_to_degree_map.keys():
                            birth = id_to_degree_map[i]
                            death = INF
                            value = (yield (birth, death, cardinalities[i] - 1))
                            del id_to_degree_map[i]

                elif value.k == 0:  # For vertices
                    # indices.insert(0, value.id)
                    cardinalities[value.id] = value.k + 1
                    id_to_degree_map[value.id] = value.degree
                    value = (yield (birth, death, dim))

                elif value.k > 0:
                    max_id = -1
                    max_degree = -1
                    boundary_obj = Boundary()

                    for sign, boundary in boundary_obj.compute_boundary(value):
                        boundary_str = ''.join([str(b) for b in boundary.kvertices])
                        id_boundary = getId(boundary_str)
                        deg_boundary = id_to_degree_map.get(id_boundary, -1)
                        if deg_boundary == -1:  # this boundary simplex has been deleted earlier. meaning this is the earliest among all the present ones.
                            max_id = -1  # A new cycle is created. This was not explained properly in the papers.
                            break
                        if max_degree < deg_boundary:
                            max_degree = deg_boundary
                            max_id = id_boundary

                    if max_id > -1:
                        # min_index = indices.index(max_id) # index of the last appearing simplex in the boundary
                        # indices.pop(min_index)
                        birth = id_to_degree_map[max_id]
                        death = value.degree
                        dim = cardinalities[max_id] - 1
                        # del cardinalities[max_id]
                        del id_to_degree_map[max_id]
                        value = (yield (birth, death, dim))

                    else:  # New cocycle. Keep it in indices.
                        # indices.insert(0, value.id)
                        cardinalities[value.id] = value.k + 1
                        id_to_degree_map[value.id] = value.degree
                        value = (yield (birth, death, dim))
            except Exception, e:
                value = e
    finally:
        # print "Don't forget to clean up when 'close()' is called."
        # del indices
        del cardinalities
        del id_to_degree_map
