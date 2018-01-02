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
        self.filtr = filtr
        self.intervals = [[] for i in range(maxdim + 1)]
        self.cc = compute_cohomology()
        b, d, dimension = self.cc.next()  # does nothing with this output. we are doing this cause we can not do send() successively unless we call .next() first

        self.maxdim = maxdim
        self.maxfilter = maxfilter

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
# def compute_cohomology(value=None):
#     """
#     Given a new incoming simplex, this function decides whether to unmark it (A new cocycle is born)
#     or mark it (An old cocyle destroyed) and yield [b,d) cycle
#     Eventually all the unmarked simplices will create [a,infty) cycles.
#     :rtype: tuple either (a,b) or (c,'inf')
#     """
#     id_to_degree_map = {}  # key = id, value = filtration appearence/degree.
#     cardinalities = {}  # key = id, value = cardinality of the simplex identfied by id
#     marked = {}  # key = id, value = True if a column identified by key is marked. False otherwise
#     # (A column is marked if this simplex contains a pivot entry)
#     zero_column = {}  # key  = id, value = True if a column identified by key is a zero-column
#     # A column is zero if it has been reduced by entries from any other columns in a row.
#     # It is non-zero if it has never been reduced.
#     # Apparantly this might be used to store the cocycle bases as well. But i will do that later.
#
#     assert isinstance(value, KSimplex) or value is None
#     isEmpty = lambda (a_list): [False, True][a_list == []]
#
#     try:
#         while True:
#             if value is None:
#                 value = (yield (-1, -1, -1))
#
#             birth = death = value.degree  # since, we ignore such cases typically.
#             dim = value.k
#             # Though theoretically its not the right thing to do.
#             try:
#
#                 if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
#                     if not marked.keys():  # signal for stoping the generator
#                         birth = death = -1
#                         value = (yield (birth, death, dim))
#                     else:
#                         for i in marked.keys():
#                             if not marked[i] and zero_column[i]:  # if unmarked process it.
#                                 birth = id_to_degree_map[i]
#                                 death = INF
#                                 value = (yield (birth, death, cardinalities[i] - 1))
#                             del marked[i]
#
#
#                 elif value.k == 0:  # Vertices
#                     cardinalities[value.id] = value.k + 1
#                     id_to_degree_map[value.id] = value.degree
#                     marked[value.id] = False  # All the vertices are UnMarked when they enter.
#                     zero_column[value.id] = True  # The vertices columns have not been reduced by any edge yet.
#                     value = (yield (birth, death, dim))
#
#                 elif value.k > 0:
#                     # Find the first boundary simplex which is  un-marked, a nonzero-column
#                     # if found, the row of value.id contains a low_R(i) for some column i.
#                     # which means the simplex value.id kills column simplex i (which is its boundary).
#                     #              1. insert the simplex value.id (not i) as a marked simplex,
#                     #              2. mark the column simplex i ( since, this column
#                     #              3. yield a [b,d) pair
#                     # if not found, then the row of value.id does not contain any pivot, a new cocycle is created (
#                     #       1. mark value.id as unmarked
#                     #       2. mark value.id as zero-column
#
#
#                     # in other words, find the latest unmarked boundary simplex [ we assume we only keep unmarked simplices]
#                     # if exists, => 1. delete this latest unmarked boundary simplex (i.e. equivalent to mark it)
#                     #               2. yield [b,d) pair
#                     # if does not exists => 1. insert simplex.id (an unmarked simplex).
#
#                     unmarked_id = -1
#                     unmarked_degree = -1
#                     boundary_obj = Boundary()
#                     # list_of_unmarked = []
#
#                     for sign, boundary in boundary_obj.compute_boundary(value):
#                         boundary_str = ''.join([str(b) for b in boundary.kvertices])
#                         id_boundary = getId(boundary_str)
#                         deg_boundary = id_to_degree_map[id_boundary]
#
#                         if marked[id_boundary]:
#                             # if zero_column.get(id_boundary,None) is not None:
#                             #     del zero_column[id_boundary]
#                             continue  # Either this column already contains a pivot entry or
#
#                             # this column is already reduced before by some other column, yet it is unmarked.
#                             # For both of these cases, we skip over those boundary simplices.
#
#                         if unmarked_degree < deg_boundary:
#                             # Now we found a zero and unmarked column which is the maximum/latest/leftmost
#                             # among all others.
#                             unmarked_degree = deg_boundary
#                             unmarked_id = id_boundary
#                             # list_of_unmarked.append(id_boundary)
#
#                     # If it is a destroyer simplex/ -ve simplex.
#                     if unmarked_id > -1:  # Found at least 1 low_R(.) in the row value.id
#                         # min_index = indices.index(max_id) # index of the last appearing simplex in the boundary
#                         # indices.pop(min_index)
#
#                         # # 2. Mark all the rest as zero if they are not marked yet.
#                         # for unmarked_and_zero_col in listof_unmarked_and_zero_cols:
#                         #     if not marked[unmarked_and_zero_col]:
#                         #         zero_column[unmarked_and_zero_col] = True
#                         #         marked[unmarked_id] = True
#
#
#                         # Check whether unmarked_id is in zero_column.
#                         if zero_column.get(unmarked_id): # yes, there is
#                             marked[unmarked_id] = True
#                             zero_column[value.id] = True
#                             id_to_degree_map[value.id] = value.degree  # insert this new simplex value.id
#                             value = (yield (-1,-1,-1))
#                         else:
#                             # for unmarked_i in list_of_unmarked:
#                             #     if unmarked_i == unmarked_id:
#                             #         continue
#                             #     zero_column[unmarked_i] = True
#
#                             birth = unmarked_degree
#                             death = value.degree
#                             dim = cardinalities[unmarked_id] - 1
#                             marked[unmarked_id] = True  # Mark this pivot column
#
#
#                             zero_column[value.id] = False
#                             zero_column[unmarked_id] = False
#
#                             # 3. Set value.id as a unmarked, non-zero-column simplex.
#                             id_to_degree_map[value.id] = value.degree # insert this new simplex value.id
#                             # coz it might be required by higher dimensional simplices for finding pivot entry
#
#                             # zero_column[value.id] = False # this value might be required by higher order simplices
#                             # # for finding pivot entry. value.id is not a 0-column coz, it might be a boundary of a higher
#                             # # order simplex.
#
#                             marked[value.id] = False # We unmark the column identified by this new simplex since, we don't
#                             # know yet, whether this is a boundary of a higher simplex or not i.e. contain a low_R(.) in its
#                             # corresponding column
#                             value = (yield (birth, death, dim))
#
#                     else:  # New cocycle. A +ve simplex/creator.
#                         # indices.insert(0, value.id)
#                         zero_column[value.id] = True
#                         cardinalities[value.id] = value.k + 1
#                         # Add value.id as an unmarked, non zero-column simplex.
#                         marked[value.id] = False
#                         id_to_degree_map[value.id] = value.degree
#                         value = (yield (birth, death, dim))
#             except Exception, e:
#                 value = e
#     finally:
#         # print "Don't forget to clean up when 'close()' is called."
#         # del indices
#         pass

# def compute_cohomology(value=None):
#     """
#     Given a new incoming simplex, this function decides whether to unmark it (A new cocycle is born)
#     or mark it (An old cocyle destroyed) and yield [b,d) cycle
#     Eventually all the unmarked simplices will create [a,infty) cycles.
#     :rtype: tuple either (a,b) or (c,'inf')
#     """
#     id_to_degree_map = {}  # key = id, value = filtration appearence/degree.
#     cardinalities = {}  # key = id, value = cardinality of the simplex identfied by id
#     marked = {}  # key = id, value = True if a column identified by key is marked. False otherwise
#     # (A column is marked if this simplex contains a pivot entry)
#     zero_column = {}  # key  = id, value = True if a column identified by key is a zero-column
#     # A column is zero if it has been reduced by entries from any other columns in a row.
#     # It is non-zero if it has never been reduced.
#     # Apparantly this might be used to store the cocycle bases as well. But i will do that later.
#
#     low = {}
#     assert isinstance(value, KSimplex) or value is None
#     isEmpty = lambda (a_list): [False, True][a_list == []]
#
#     try:
#         while True:
#             if value is None:
#                 value = (yield (-1, -1, -1))
#
#             birth = death = value.degree  # since, we ignore such cases typically.
#             dim = value.k
#             # Though theoretically its not the right thing to do.
#             try:
#
#                 if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
#                     if not low.keys():  # signal for stoping the generator
#                         birth = death = -1
#                         value = (yield (birth, death, dim))
#                     else:
#                         for i in low.keys():
#                             if low[i] == INF:  # if unmarked process it.
#                                 birth = id_to_degree_map[i]
#                                 death = INF
#                                 value = (yield (birth, death, cardinalities[i] - 1))
#                             del low[i]
#
#
#                 elif value.k == 0:  # Vertices
#                     cardinalities[value.id] = value.k + 1
#                     id_to_degree_map[value.id] = value.degree
#                     marked[value.id] = False  # All the vertices are UnMarked when they enter.
#                     zero_column[value.id] = True  # The vertices columns have not been reduced by any edge yet.
#                     value = (yield (birth, death, dim))
#
#                 elif value.k > 0:
#                     # Find the first boundary simplex which is  un-marked, a nonzero-column
#                     # if found, the row of value.id contains a low_R(i) for some column i.
#                     # which means the simplex value.id kills column simplex i (which is its boundary).
#                     #              1. insert the simplex value.id (not i) as a marked simplex,
#                     #              2. mark the column simplex i ( since, this column
#                     #              3. yield a [b,d) pair
#                     # if not found, then the row of value.id does not contain any pivot, a new cocycle is created (
#                     #       1. mark value.id as unmarked
#                     #       2. mark value.id as zero-column
#
#
#                     # in other words, find the latest unmarked boundary simplex [ we assume we only keep unmarked simplices]
#                     # if exists, => 1. delete this latest unmarked boundary simplex (i.e. equivalent to mark it)
#                     #               2. yield [b,d) pair
#                     # if does not exists => 1. insert simplex.id (an unmarked simplex).
#
#                     unmarked_id = -1
#                     unmarked_degree = -1
#                     boundary_obj = Boundary()
#                     # list_of_unmarked = []
#
#                     for sign, boundary in boundary_obj.compute_boundary(value):
#                         boundary_str = ''.join([str(b) for b in boundary.kvertices])
#                         id_boundary = getId(boundary_str)
#                         deg_boundary = id_to_degree_map[id_boundary]
#
#                         if marked[id_boundary]:
#                             # if zero_column.get(id_boundary,None) is not None:
#                             #     del zero_column[id_boundary]
#                             continue  # Either this column already contains a pivot entry or
#                         else:
#                             if low.get(id_boundary, None) is None:
#                                 low[id_boundary] = deg_boundary
#
#                         if unmarked_degree < deg_boundary:
#                             # Now we found a zero and unmarked column which is the maximum/latest/leftmost
#                             # among all others.
#                             unmarked_degree = deg_boundary
#                             unmarked_id = id_boundary
#                             # list_of_unmarked.append(id_boundary)
#
#                     # If it is a destroyer simplex/ -ve simplex.
#                     if unmarked_id > -1 and low[unmarked_id] < value.degree:
#                         # Found at least 1 low_R(.) in the row value.id
#                         # min_index = indices.index(max_id) # index of the last appearing simplex in the boundary
#                         # indices.pop(min_index)
#
#                         # # 2. Mark all the rest as zero if they are not marked yet.
#                         # for unmarked_and_zero_col in listof_unmarked_and_zero_cols:
#                         #     if not marked[unmarked_and_zero_col]:
#                         #         zero_column[unmarked_and_zero_col] = True
#                         #         marked[unmarked_id] = True
#
#
#                         # Check whether unmarked_id is in zero_column.
#
#                         birth = unmarked_degree
#                         death = value.degree
#                         dim = cardinalities[unmarked_id] - 1
#                         marked[unmarked_id] = True  # Mark this pivot column
#
#                         # zero_column[value.id] = False
#                         # zero_column[unmarked_id] = False
#                         #
#                         # # 3. Set value.id as a unmarked, non-zero-column simplex.
#                         # id_to_degree_map[value.id] = value.degree  # insert this new simplex value.id
#                         # # coz it might be required by higher dimensional simplices for finding pivot entry
#                         #
#                         # # zero_column[value.id] = False # this value might be required by higher order simplices
#                         # # # for finding pivot entry. value.id is not a 0-column coz, it might be a boundary of a higher
#                         # # # order simplex.
#                         #
#                         marked[value.id] = False  # We unmark the column identified by this new simplex since, we don't
#                         # know yet, whether this is a boundary of a higher simplex or not i.e. contain a low_R(.) in its
#                         # corresponding column
#                         value = (yield (birth, death, dim))
#
#                     else:  # New cocycle. A +ve simplex/creator.
#                         # indices.insert(0, value.id)
#                         zero_column[value.id] = True
#                         cardinalities[value.id] = value.k + 1
#                         # Add value.id as an unmarked, non zero-column simplex.
#                         marked[value.id] = False
#                         id_to_degree_map[value.id] = value.degree
#                         value = (yield (birth, death, dim))
#             except Exception, e:
#                 value = e
#     finally:
#         # print "Don't forget to clean up when 'close()' is called."
#         # del indices
#         pass


# def compute_cohomology(value=None):
#     id_to_degree_map = {}  # key = id, value = filtration appearence/degree.
#     cardinalities = {}  # key = id, value = cardinality of the simplex identfied by id
#     marked = {}  # key = id, value = True if a column identified by key is marked. False otherwise
#     # (A column is marked if this simplex contains a pivot entry)
#     zero_column = {}  # key  = id, value = True if a column identified by key is a zero-column
#     # A column is zero if it has been reduced by entries from any other columns in a row.
#     # It is non-zero if it has never been reduced.
#     # Apparantly this might be used to store the cocycle bases as well. But i will do that later.
#
#     low = {}
#     assert isinstance(value, KSimplex) or value is None
#     isEmpty = lambda (a_list): [False, True][a_list == []]
#
#     try:
#         while True:
#             if value is None:
#                 value = (yield (-1, -1, -1))
#
#             birth = death = value.degree  # since, we ignore such cases typically.
#             dim = value.k
#             # Though theoretically its not the right thing to do.
#             try:
#
#                 if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
#                     if not low.keys():  # signal for stoping the generator
#                         birth = death = -1
#                         value = (yield (birth, death, dim))
#                     else:
#                         for i in low.keys():
#                             if low[i] == INF:  # if unmarked process it.
#                                 birth = id_to_degree_map[i]
#                                 death = INF
#                                 value = (yield (birth, death, cardinalities[i] - 1))
#                             del low[i]
#
#
#                 elif value.k == 0:  # Vertices
#                     cardinalities[value.id] = value.k + 1
#                     id_to_degree_map[value.id] = value.degree
#                     marked[value.id] = False  # All the vertices are UnMarked when they enter.
#                     zero_column[value.id] = True  # The vertices columns have not been reduced by any edge yet.
#                     value = (yield (birth, death, dim))
#
#                 elif value.k > 0:
#                     # Find the first boundary simplex which is  un-marked, a nonzero-column
#                     # if found, the row of value.id contains a low_R(i) for some column i.
#                     # which means the simplex value.id kills column simplex i (which is its boundary).
#                     #              1. insert the simplex value.id (not i) as a marked simplex,
#                     #              2. mark the column simplex i ( since, this column
#                     #              3. yield a [b,d) pair
#                     # if not found, then the row of value.id does not contain any pivot, a new cocycle is created (
#                     #       1. mark value.id as unmarked
#                     #       2. mark value.id as zero-column
#
#
#                     # in other words, find the latest unmarked boundary simplex [ we assume we only keep unmarked simplices]
#                     # if exists, => 1. delete this latest unmarked boundary simplex (i.e. equivalent to mark it)
#                     #               2. yield [b,d) pair
#                     # if does not exists => 1. insert simplex.id (an unmarked simplex).
#
#                     unmarked_id = -1
#                     unmarked_degree = -1
#                     boundary_obj = Boundary()
#                     # list_of_unmarked = []
#
#                     for sign, boundary in boundary_obj.compute_boundary(value):
#                         boundary_str = ''.join([str(b) for b in boundary.kvertices])
#                         id_boundary = getId(boundary_str)
#                         deg_boundary = id_to_degree_map[id_boundary]
#
#                         if marked[id_boundary]:
#                             # if zero_column.get(id_boundary,None) is not None:
#                             #     del zero_column[id_boundary]
#                             continue  # Either this column already contains a pivot entry or
#                         else:
#                             if low.get(id_boundary, None) is None:
#                                 low[id_boundary] = deg_boundary
#
#                         if unmarked_degree < deg_boundary:
#                             # Now we found a zero and unmarked column which is the maximum/latest/leftmost
#                             # among all others.
#                             unmarked_degree = deg_boundary
#                             unmarked_id = id_boundary
#                             # list_of_unmarked.append(id_boundary)
#
#                     # If it is a destroyer simplex/ -ve simplex.
#                     if unmarked_id > -1 and low[unmarked_id] < value.degree:
#                         # Found at least 1 low_R(.) in the row value.id
#                         # min_index = indices.index(max_id) # index of the last appearing simplex in the boundary
#                         # indices.pop(min_index)
#
#                         # # 2. Mark all the rest as zero if they are not marked yet.
#                         # for unmarked_and_zero_col in listof_unmarked_and_zero_cols:
#                         #     if not marked[unmarked_and_zero_col]:
#                         #         zero_column[unmarked_and_zero_col] = True
#                         #         marked[unmarked_id] = True
#
#
#                         # Check whether unmarked_id is in zero_column.
#
#                         birth = unmarked_degree
#                         death = value.degree
#                         dim = cardinalities[unmarked_id] - 1
#                         marked[unmarked_id] = True  # Mark this pivot column
#
#                         # zero_column[value.id] = False
#                         # zero_column[unmarked_id] = False
#                         #
#                         # # 3. Set value.id as a unmarked, non-zero-column simplex.
#                         # id_to_degree_map[value.id] = value.degree  # insert this new simplex value.id
#                         # # coz it might be required by higher dimensional simplices for finding pivot entry
#                         #
#                         # # zero_column[value.id] = False # this value might be required by higher order simplices
#                         # # # for finding pivot entry. value.id is not a 0-column coz, it might be a boundary of a higher
#                         # # # order simplex.
#                         #
#                         marked[value.id] = False  # We unmark the column identified by this new simplex since, we don't
#                         # know yet, whether this is a boundary of a higher simplex or not i.e. contain a low_R(.) in its
#                         # corresponding column
#                         value = (yield (birth, death, dim))
#
#                     else:  # New cocycle. A +ve simplex/creator.
#                         # indices.insert(0, value.id)
#                         zero_column[value.id] = True
#                         cardinalities[value.id] = value.k + 1
#                         # Add value.id as an unmarked, non zero-column simplex.
#                         marked[value.id] = False
#                         id_to_degree_map[value.id] = value.degree
#                         value = (yield (birth, death, dim))
#             except Exception, e:
#                 value = e
#     finally:
#         # print "Don't forget to clean up when 'close()' is called."
#         # del indices
#         pass

def compute_cohomology(value=None):
    id_to_degree_map = {}  # key = id, value = filtration appearence/degree.
    cardinalities = {}
    unmarked = {}  # key = card value = list [] of unmarked simplices of that cardinality
    unmarked_basis = {}  # key = id, value = set of ids

    try:
        while True:
            if value is None:
                value = (yield (-1, -1, -1))

            birth = death = value.degree  # since, we ignore such cases typically.
            dim = value.k
            # Though theoretically its not the right thing to do.
            try:
                if value.k < 0:  # meaning i want to just go throw indices for infinity intervals
                    flag = False
                    for card in unmarked.keys():
                        for id_sigma in unmarked.get(card, []):
                            birth = id_to_degree_map[id_sigma]
                            death = INF
                            flag = True
                            value = (yield (birth, death, card - 1))
                            unmarked[card].remove(id_sigma)

                    if flag is False:
                        yield (-1, -1, -1)

                elif value.k == 0:  # Vertices
                    cardinalities[value.id] = value.k + 1
                    id_to_degree_map[value.id] = value.degree

                    list_of_unmarked = unmarked.get(value.k + 1, [])
                    if list_of_unmarked:
                        unmarked[value.k + 1].append(value.id)
                    else:
                        unmarked[value.k + 1] = [value.id]

                    unmarked_basis[value.id] = set([value.id])
                    value = (yield (birth, death, dim))

                else:  # 1-simplex, 2-simplex, etc.
                    destroyer_flag = False
                    most_recently_killed_degree = -1
                    most_recently_killed_id = -1
                    list_bases_toupdate = []  # list of id whose bases needs update
                    boundary_obj = Boundary()
                    # list_of_unmarked = []

                    boundary_set = set([])
                    card_boundary = value.k
                    for sign, boundary in boundary_obj.compute_boundary(value):
                        boundary_str = ''.join([str(b) for b in boundary.kvertices])
                        id_boundary = getId(boundary_str)
                        boundary_set = boundary_set.union([id_boundary])

                    # for each simplex of cardinality card_boundary, check whether
                    # the corresponding boundary set intersection is empty or have cardinality even
                    for id_sigma in unmarked.get(card_boundary, []):
                        basis_sigma = unmarked_basis.get(id_sigma)
                        intersecting_set = basis_sigma.intersection(boundary_set)
                        len_intersecting_set = len(intersecting_set)
                        if len_intersecting_set % 2:  # odd => destroyer
                            destroyer_flag = True
                            list_bases_toupdate.append(id_sigma)
                            if id_to_degree_map[id_sigma] > most_recently_killed_degree:
                                most_recently_killed_id = id_sigma
                                most_recently_killed_degree = id_to_degree_map[id_sigma]

                    # If it is a destroyer simplex/ -ve simplex.
                    if destroyer_flag:
                        birth = most_recently_killed_degree
                        death = value.degree
                        dim = cardinalities[most_recently_killed_id] - 1

                        unmarked[dim + 1].remove(most_recently_killed_id)

                        # update the bases for all ids in list_bases_toupdate except most_recently_killed_id
                        for id in list_bases_toupdate:
                            if id != most_recently_killed_id:
                                unmarked_basis[id].symmetric_difference_update(unmarked_basis[most_recently_killed_id])

                        del unmarked_basis[most_recently_killed_id]

                        unmarked_basis[value.id] = set([value.id])
                        id_to_degree_map[value.id] = value.degree

                        value = (yield (birth, death, dim))

                    else:  # New cocycle. A +ve simplex/creator.
                        cardinalities[value.id] = value.k + 1

                        list_of_unmarked = unmarked.get(value.k + 1, [])
                        if list_of_unmarked:
                            unmarked[value.k + 1].append(value.id)
                        else:
                            unmarked[value.k + 1] = [value.id]

                        unmarked_basis[value.id] = set([value.id])
                        id_to_degree_map[value.id] = value.degree

                        value = (yield (birth, death, dim))

                        # we must add the basis for value.id irrespective of it being creator or destroyer

            except Exception, e:
                value = e
    finally:
        # print "Don't forget to clean up when 'close()' is called."
        # del indices
        pass
