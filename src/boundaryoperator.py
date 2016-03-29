from simplex import KSimplex


class Boundary:
    def __init__(self):
        self.boundary = []

    def compute_boundary(self, k_simplex):
        '''
        Computes the boundary of a k_simplex.
        :param k_simplex: KSimplex object
        '''
        # if k_simplex.k == 1:
        #   return (0,)
        indexlist = k_simplex.kvertices
        start = 0
        end = len(indexlist)
        mid = 0
        if end == 1:
            return []
        for mid in range(start, end):
            self.boundary.append(((1) ** mid, KSimplex(indexlist[start:mid] + indexlist[mid + 1:end])))
        return self.boundary

    def get_boundary(self):
        '''
        Returns the boundary of the K-simplex
        :return: list of tuples like ( sign(+ or -) , K-Simplex Object )
        '''
        return self.boundary

    def __str__(self):
        str_repr = ''
        for sign, simplex in self.boundary:
            str_repr += (['+', '-'][sign == -1] + str(simplex.kvertices) + " ")

        return str_repr

    '''
class boundaryinz2:
    def __init__(self,simpl_indx_map):
        self.boundary = []
        self.map  = simpl_indx_map # array of ksimplex

    def compute_boundary(self, k_simplex):


        indexlist = k_simplex.kvertices
        sigmak = k_simplex.k
        start = 0
        end = len(indexlist)
        mid = 0
        self.ksimplex_to_indexmap = {}

        for i in range(len(self.filt.listof_iFiltration)):
            for ksimplex in self.filt.get_ksimplices_from_ithFiltration(sigmak-1,i):
                if ksimplex:
                    self.ksimplex_to_indexmap[tuple(ksimplex.kvertices)] = x.degree

        for mid in range(start, end):
            self.boundary.append(((1) ** mid , KSimplex(indexlist[start:mid] + indexlist[mid + 1:end])))

    def get_boundary(self):

        return self.boundary

    def get_maxindex(self):
        maxk_index = -1
        m
        print self.boundaryaxsig = None
sign,        for sig in self.boundary:
            sig_kindex = self.ksimplex_tuple(exm.kvertices)g.kvertices)]
            if sig_kindex > maxk_index:
                maxk_index = sig_kindex
                maxsig = sig
        return (maxk_index,maxsig)


    def remove_simplex(self,sigma):
        del self.ksimplex_to_indexmap[tuple(sigma.kvertices)] #only deleting from hashtable. not from boundary[] list

    def __str__(self):
        str_repr = ''
        for sign, simplex in self.boundary:
            str_repr += (['+', '-'][sign == -1] + str(simplex.kvertices) + " ")

        return str_repr

    '''
