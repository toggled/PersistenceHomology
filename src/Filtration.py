from src.simplex import SimplicialComplex, KSimplex
from memory_profiler import profile

__author__ = 'Naheed'


class iFiltration:
    def __init__(self, index):
        self.index = index  # Filtration index
        self.simplicial_complex = SimplicialComplex()
        self.value = index

    def set_value(self, filtration_value):
        self.value = filtration_value

    def add_simplex_to_filtration(self, simplex):
        '''
        :param s`implex: An instance of KSimplex
        :return:
        '''
        self.simplicial_complex.add_simplex(simplex)

    def get_all_ksimplices(self, k):
        return self.simplicial_complex.get_allkth_simplices(k)

    def has_simplex(self, Ksim):
        assert isinstance(Ksim, KSimplex)
        k = Ksim.k
        for sim in self.simplicial_complex.get_allkth_simplices(k):
            if sim == Ksim:
                return True
        return False

    def __len__(self):
        return len(self.simplicial_complex)

    def __str__(self):
        # return str(self.simplicial_complex)+"\n"+"Size: "+str(len(self.simplicial_complex))
        return str(self.simplicial_complex)


class Filtration:
    """
    This is an integer indexed filtration
    """

    def __init__(self):
        self.listof_iFiltration = {}
        # This map is needed in the dk matrix formation coz we need degree
        self.simplex_to_filtrationmap = {}
        self.maxdeg = 0

    def add_filtration(self, i):
        self.listof_iFiltration[i] = iFiltration(i)

    def add_filtrationwithvalue(self, i, val):
        self.listof_iFiltration[i] = iFiltration(i)
        self.listof_iFiltration[i].set_value(val)

    def get_ithfiltration(self, i):
        return self.listof_iFiltration.get(i, None)

    def get_ksimplices_from_ithFiltration(self, k, i):
        '''
        :param k: K-simplices
        :param i: i-th filtration
        :return: List of Simplex objects from the simplicial complex at i-th filtration
        '''
        return self.get_ithfiltration(i).get_all_ksimplices(k)

    def has_ksimplex_in_ithfiltration(self, KSim, i):
        assert isinstance(KSim, KSimplex)
        return self.get_ithfiltration(i).has_simplex(KSim)

    def add_simplex_toith_filtration(self, i, simplex):
        '''
        :param i: i'th Filtration
        :param simplex: Simplex to add to i'th Filtration may be a list or a KSimplex instance
        :return: None
        '''
        # IF the ifiltration is None create it
        if self.listof_iFiltration.get(i, None) is None:
            self.add_filtration(i)

        # If its a KSimplex instance
        if isinstance(simplex, KSimplex):
            if simplex.degree is None:
                simplex.degree = i
            self.listof_iFiltration[i].add_simplex_to_filtration(simplex)
            self.simplex_to_filtrationmap[tuple(simplex.kvertices)] = i
        else:
            ksimplex = KSimplex(simplex, i)
            self.listof_iFiltration[i].add_simplex_to_filtration(ksimplex)
            self.simplex_to_filtrationmap[
                tuple(ksimplex.kvertices)] = i  # An already added simplex may be overriden by the same
            # itself if it occurs in a later filtration
            # Do we allow this?

    def add_simplices_from_file(self, filename):
        with open(filename, 'r') as fp:
            while 1:
                line = fp.readline()
                if not line:
                    break
                simplex, filtr_idx = line.split(',')
                # Building the K-simplex object .
                # I better insert them in sorted order to avoid orientation conflict
                # between higher dimensional simplices.
                ksimplex_obj = KSimplex(sorted([int(v) for v in
                                                simplex.split()]))
                self.add_simplex_toith_filtration(int(filtr_idx), ksimplex_obj)
                self.maxdeg = max(self.maxdeg, int(filtr_idx))

    def add_simplices_from_cliquefiles(self, dir):
        base = 'clique_'
        from os import listdir
        for fil in listdir(dir):
            if fil.startswith(base):
                filtr_idx = int(fil.split("_")[1][0])
                print 'adding filtration: ' + str(filtr_idx)
                with open(dir + '/' + fil, 'r') as fp:
                    while 1:
                        simplex = fp.readline()
                        # print simplex
                        if not simplex:
                            break
                        ksimplex_obj = KSimplex(sorted(int(v) for v in simplex.split()))
                        added_already = False
                        for i in xrange(filtr_idx - 1):
                            if self.has_ksimplex_in_ithfiltration(ksimplex_obj, i):
                                added_already = True

                        if not added_already:
                            self.add_simplex_toith_filtration(filtr_idx - 1, ksimplex_obj)

    def __str__(self):
        repr = ''
        for key, val in sorted(self.listof_iFiltration.items()):
            repr += "Filtration " + str(key) + '\n' + str(val) + "\n"

        return repr

    def __len__(self):
        return sum([len(a) for a in self.listof_iFiltration.values()])

    def write_boundarylists_to(self, filename):
        """
        Writes a real valued filtration to a .fil file. We need to write a filtration first if later we
        want to read filtration by chunk.
        The format is:-
        Each line:- simplex-id,Its Boundary(the id of the simplices seperated by space),filtration value,
        dimension of the simplex
        """
        from src.boundaryoperator import Boundary
        with open(filename,"w+") as fp:
            for i in range(len(self.listof_iFiltration)):
                ith_fil = self.get_ithfiltration(i)
                fil_value = str(i)
                assert isinstance(ith_fil, iFiltration)
                for sigma in ith_fil.simplicial_complex.simplex:
                    assert isinstance(sigma, KSimplex)
                    simplex_id = sigma.id
                    bd = Boundary()
                    bd.compute_boundary(sigma)
                    bd_list = []
                    for sign, face in bd.get_boundary():
                        assert isinstance(face, KSimplex)
                        bd_list.append(face.id)
                    bd_str = ' '.join(bd_list)
                    fp.write(simplex_id + "," + bd_str + "," + fil_value + "," + str(sigma.k) + "\n")

class RealvaluedFiltration(object):
    """
        A filtration where each iFiltration has real value
    """

    def __init__(self, filtration_values):
        self.listof_iFiltration = {}
        # This map is needed in the dk matrix formation coz we need degree
        self.simplex_to_filtrationmap = {}
        self.maxdeg = 0
        self.filtration_values = filtration_values
        self.maxfiltration_val = filtration_values[-1]  # largest filtration value
        self.diff_filtrationval = filtration_values[1] - filtration_values[
            0]  # difference in consecutive filtration values

    def add_filtration(self, i):
        self.listof_iFiltration[i] = iFiltration(i)

    def add_filtrationwithvalue(self, i, val):
        self.listof_iFiltration[i] = iFiltration(i)
        assert val <= self.maxfiltration_val
        self.listof_iFiltration[i].set_value(val)

    def get_ithfiltration(self, i):
        ithFilt = self.listof_iFiltration.get(i, None)
        if ithFilt is None:
            return []
        return ithFilt

    def get_ksimplices_from_ithFiltration(self, k, i):
        '''
        :param k: K-simplices
        :param i: i-th filtration
        :return: List of Simplex objects from the simplicial complex at i-th filtration
        '''
        ith_Filtration = self.get_ithfiltration(i)
        if not ith_Filtration:
            return []
        return ith_Filtration.get_all_ksimplices(k)

    def has_ksimplex_in_ithfiltration(self, KSim, i):
        assert isinstance(KSim, KSimplex)
        return self.get_ithfiltration(i).has_simplex(KSim)

    def add_simplex_toith_filtration(self, i, filtration_val, simplex):
        '''
        This function does not make sure whether sub-faces are present in the filtration or not.
        It is the responsibility of the caller function to ensure that.
        :rtype: object
        :param i: i'th Filtration
        :param filtration_val: value of the i'th filtration
        :param simplex: Simplex to add to i'th Filtration may be a list or a KSimplex instance
        :return: None
        '''
        # IF the ifiltration is None create it
        if self.listof_iFiltration.get(i, None) is None:
            self.add_filtrationwithvalue(i, filtration_val)

        # If its a KSimplex instance
        if isinstance(simplex, KSimplex):
            if simplex.degree is None:
                simplex.degree = filtration_val
            self.listof_iFiltration[i].add_simplex_to_filtration(simplex)
            self.simplex_to_filtrationmap[tuple(simplex.kvertices)] = i
        else:
            ksimplex = KSimplex(simplex, filtration_val)
            self.listof_iFiltration[i].add_simplex_to_filtration(ksimplex)
            self.simplex_to_filtrationmap[tuple(ksimplex.kvertices)] = i

    # def add_simplices_from_file(self, filename):
    #     with open(filename, 'r') as fp:
    #         while 1:
    #             line = fp.readline()
    #             if not line:
    #                 break
    #             simplex, filtr_idx = line.split(',')
    # Building the K-simplex object .
    # Always insert them in sorted order to avoid orientation conflict
    # between higher dimensional simplices.
    #             ksimplex_obj = KSimplex(sorted([int(v) for v in
    #                                             simplex.split()]))
    #             self.add_simplex_toith_filtration(int(filtr_idx), ksimplex_obj)

    # def add_simplices_from_cliquefiles(self, dir):
    #     base = 'clique_'
    #     from os import path, listdir
    #     for fil in listdir(dir):
    #         if fil.startswith(base):
    #             filtr_idx = int(fil.split("_")[1][0])
    #             print 'adding filtration: ' + str(filtr_idx)
    #             with open(dir + '/' + fil, 'r') as fp:
    #                 while 1:
    #                     simplex = fp.readline()
    #                     # print simplex
    #                     if not simplex:
    #                         break
    #                     ksimplex_obj = KSimplex(sorted(int(v) for v in simplex.split()))
    #                     added_already = False
    #                     for i in xrange(filtr_idx - 1):
    #                         if self.has_ksimplex_in_ithfiltration(ksimplex_obj, i):
    #                             added_already = True
    #
    #                     if not added_already:
    #                         self.add_simplex_toith_filtration(filtr_idx - 1, ksimplex_obj)

    def __str__(self):
        repr = ''
        for key, val in sorted(self.listof_iFiltration.items()):
            repr += "Filtration " + str(key) + ": " + '\n' + str(val) + "\n"

        return repr

    def __len__(self):
        """
        Returns the total number of simplices in the filtration
        """
        return sum([len(a) for a in self.listof_iFiltration.values()])

    def write_boundarylists_to(self,filename):
        """
        Writes a real valued filtration to a .fil file. We need to write a filtration first if later we
        want to read filtration by chunk.
        The format is:-
        Each line:- simplex-id,Its Boundary(the id of the simplices seperated by space),filtration value,
        dimension of the simplex
        """
        from src.boundaryoperator import Boundary
        with open(filename,'w+') as fp:
            for i in range(len(self.listof_iFiltration)):
                ith_fil = self.get_ithfiltration(i)
                fil_value = str(self.filtration_values[i])
                # assert isinstance(ith_fil,iFiltration)
                if not ith_fil:
                    continue
                for sigma in ith_fil.simplicial_complex.simplex:
                    assert isinstance(sigma,KSimplex)
                    simplex_id = sigma.id
                    bd = Boundary()
                    bd.compute_boundary(sigma)
                    bd_list = []
                    for sign,face in bd.get_boundary():
                        assert isinstance(face,KSimplex)
                        bd_list.append(face.id)
                    bd_str = ' '.join(bd_list)
                    fp.write(simplex_id+","+bd_str+","+fil_value+","+str(sigma.k)+"\n")




