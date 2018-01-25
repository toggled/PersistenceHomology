"""
pHRow algorithm as described in paper:- DUALITIES IN PERSISTENT (CO)HOMOLOGY
This algorithm starts from simplices of last filtration to the first.
For each simplex compute its coboundary. Find the latest appearing simplex in its coboundary. And reduce the rest of the
simplices which appeared earlier.
"""
from memory_profiler import profile
# from profilestats import profile

__author__ = 'Naheed'

from src.simplex import KSimplex
from src.boundaryoperator import Boundary
from idmanager import getId

INF = float('inf')


class FiltrationArrayCohomologyComputer():
    """
    Given a filtration and its parameters, provides functionality to compute persistent cohomology
     using the algorithm pCoh as described in "Persistent Cohomology and Circular Coordinates" paper.
    """

    def __init__(self, filtr, maxdim, maxfilter):
        self.intervals = [[] for i in range(maxdim + 1)]
        self.maxdim = maxdim
        self.maxfilter = maxfilter

        self.filtration_ar = []  # ordered list of simplices in the filtration
        self.simplexid_to_indexmap = {}  # this map is very useful. for disk based implementation it can be used as
        # inverted index where the values become pointer instead of positive int.
        # we know a simplices degree, id, cardinality/size all from this map
        dummy_counter = 0
        for k in xrange(self.maxdim + 1):
            for i in filtr.listof_iFiltration.keys():
                for ksimplex in filtr.get_ksimplices_from_ithFiltration(k, i):
                    assert isinstance(ksimplex, KSimplex)
                    if ksimplex and ksimplex.degree <= self.maxfilter:
                        self.filtration_ar.append(ksimplex)
                        self.simplexid_to_indexmap[ksimplex.id] = dummy_counter
                        dummy_counter += 1

    # @profile
    def compute(self):
        """
        Compute the persistent cohomology
        """
        unmarked = {}  # key = card value = list [] of unmarked simplices' id of that cardinality
        unmarked_basis = {}  # key = id, value = set of ids whose linear combination makes the basis

        for sigma in self.filtration_ar:
            if sigma.k == 0:  # Vertices
                list_of_unmarked = unmarked.get(sigma.k + 1, [])
                if list_of_unmarked:
                    if sigma.id not in unmarked[sigma.k + 1]:
                        unmarked[sigma.k + 1].append(sigma.id)  # avoid repeatedly storing an id
                        unmarked_basis[sigma.id] = {sigma.id}
                else:
                    unmarked[sigma.k + 1] = [sigma.id]
                    unmarked_basis[sigma.id] = {sigma.id}


            else:
                destroyer_flag = False
                most_recently_killed_degree = -1
                most_recently_killed_id = -1
                list_bases_toupdate = []  # list of id whose bases needs update
                boundary_obj = Boundary()
                # list_of_unmarked = []

                boundary_set = set([])
                card_boundary = sigma.k
                for sign, boundary in boundary_obj.compute_boundary(sigma):
                    # constuct string repr of the simplex
                    boundary_str = '|'.join([str(b) for b in boundary.kvertices])
                    id_boundary = getId(boundary_str)
                    boundary_set = boundary_set.union([id_boundary])

                # for each simplex of cardinality card_boundary, check whether
                # the corresponding boundary set intersection is empty or have even cardinality
                for id_sigma in unmarked.get(card_boundary, []):
                    basis_sigma = unmarked_basis.get(id_sigma)
                    intersecting_set = basis_sigma.intersection(boundary_set)
                    len_intersecting_set = len(intersecting_set)
                    if len_intersecting_set % 2:  # odd => destroyer
                        destroyer_flag = True
                        list_bases_toupdate.append(id_sigma)
                        deg_id_sigma = self.filtration_ar[self.simplexid_to_indexmap[id_sigma]].degree
                        if deg_id_sigma > most_recently_killed_degree:
                            most_recently_killed_id = id_sigma
                            most_recently_killed_degree = deg_id_sigma
                        # else:
                        #     # When both id_sigma and most_recently_killed_id have same degree, we resolve the ordering
                        #     # by their index in the filtration_ar
                        #     if self.simplexid_to_indexmap[id_sigma] > self.simplexid_to_indexmap[
                        #         most_recently_killed_id] and deg_id_sigma == most_recently_killed_degree:
                        #         most_recently_killed_id = id_sigma
                        #         most_recently_killed_degree = deg_id_sigma

                # If it is a destroyer simplex/ -ve simplex.
                if destroyer_flag:
                    birth = most_recently_killed_degree
                    death = sigma.degree
                    simplex_index = self.simplexid_to_indexmap[most_recently_killed_id]
                    simplex_to_destroy = self.filtration_ar[simplex_index]
                    assert isinstance(simplex_to_destroy, KSimplex)
                    dim = simplex_to_destroy.k
                    self.intervals[dim].append((birth, death))


                    # mark this id. we only keep unmarked ids, unmarked == pivot
                    unmarked[dim + 1].remove(most_recently_killed_id)


                    # update the bases for all ids in list_bases_toupdate except most_recently_killed_id
                    for id in list_bases_toupdate:
                        if id != most_recently_killed_id:
                            unmarked_basis[id].symmetric_difference_update(unmarked_basis[most_recently_killed_id])

                    del unmarked_basis[most_recently_killed_id]

                    unmarked_basis[sigma.id] = {sigma.id}

                else:  # New cocycle. A +ve simplex/creator.
                    list_of_unmarked = unmarked.get(sigma.k + 1, [])
                    if list_of_unmarked:
                        if sigma.id not in unmarked[sigma.k + 1]:
                            unmarked[sigma.k + 1].append(sigma.id)
                            unmarked_basis[sigma.id] = {sigma.id}
                    else:
                        unmarked[sigma.k + 1] = [sigma.id]
                        unmarked_basis[sigma.id] = {sigma.id}


        for card in unmarked.keys():
            for id_sigma in unmarked.get(card, []):
                birth = self.filtration_ar[self.simplexid_to_indexmap[id_sigma]].degree
                death = INF
                self.intervals[card - 1].append((birth, death))


    def print_BettiNumbers(self):
        repr = ''
        for dim, li in enumerate(self.intervals):
            repr += ('dim: ' + str(dim) + '\n')
            for tup in li:
                if tup[0] == tup[1]:
                    continue
                repr += str(tup)
            repr += '\n'
        print repr

    def compare(self, phom_intervals):
        """
        Compares two intervals whether they are equal
        """
        # print sorted(phom_intervals)
        # print sorted(self.intervals)
        for dim,li in enumerate(phom_intervals):
            for pair in li:
                if pair in self.intervals[0]:
                    try:
                        self.intervals[0].remove(pair)
                    except:
                        return False
            if len(self.intervals[0]) == 0:
                self.intervals.remove([])

        if len(self.intervals):
            return False

        return True