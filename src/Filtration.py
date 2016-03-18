from src.simplex import SimplicialComplex, KSimplex

__author__ = 'Naheed'

class iFiltration:
    def __init__(self,index):
        self.index = index # Filtration index
        self.simplicial_complex = SimplicialComplex()

    def add_simplex_to_filtration(self,simplex):
        '''

        :param filtration_index: The index of the filtration
        :param simplex: An instance of KSimplex
        :return:
        '''
        self.simplicial_complex.add_simplex(simplex)

    def __str__(self):
        return str(self.simplicial_complex)

class Filtration:
    def __init__(self):
        self.listof_iFiltration = {}

    def add_filtration(self,i):
        self.listof_iFiltration[i] = iFiltration(i)

    def get_ithfiltration(self,i):
        return self.listof_iFiltration.get(i,None)

    def add_simplex_toith_filtration(self,i,simplex):
        '''
        :param i: i'th Filtration
        :param simplex: Simplex to add to i'th Filtration may be a list or a KSimplex instance
        :return: None
        '''
        # IF the ifiltration is None create it
        if self.listof_iFiltration.get(i,None) is None:
            self.add_filtration(i)

        # If its a KSimplex instance
        if isinstance(simplex, KSimplex):
            if simplex.degree is None:
                simplex.degree = i
            self.listof_iFiltration[i].add_simplex_to_filtration(simplex)
        else:
            ksimplex = KSimplex(simplex,i)
            self.listof_iFiltration[i].add_simplex_to_filtration(ksimplex)

    def add_simplices_from_file(self,filename):
        with open(filename, 'r') as fp:
            while 1:
                line = fp.readline()
                if not line:
                    break
                simplex, filtr_idx = line.split(',')
                ksimplex_obj = KSimplex(sorted([int(v) for v in
                                                simplex.split()]))  # Building the K-simplex object . Always insert them in sorted order to avoid orientation conflict between higher dimensional simplices.
                self.add_simplex_toith_filtration(filtr_idx,ksimplex_obj)

    def __str__(self):
        repr = ''
        for key,val in sorted(self.listof_iFiltration.items()):

            repr += "Filtration "+str(key)+'\n'+str(val)+"\n"

        return repr
