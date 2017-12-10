from src.idmanager import getId
class KSimplex:
    def __init__(self, listofvertices, degree=None):
        if listofvertices == []:
            self.k = -1
            self.degree = -1
            return
        if type(listofvertices[0]) == str:
            self.kvertices = [int(i) for i in listofvertices]
            self.id = getId(''.join(listofvertices))
        else:
            self.kvertices = sorted(listofvertices)
            self.id = getId(''.join([str(i) for i in self.kvertices]))

        self.k = len(listofvertices) - 1
        self.name = str(self.k) + '-simplex: ' + str(listofvertices)
        # This id is used as index while building transformation matrix
        self.degree = degree  # Degree of a KSimplex is like arrival time of that ksimplex in the simpcompne
        # For Integer indexed filtration degree will be integer, real valued for real valued filtration

    def __str__(self):
        # return nice string representation of the k-simplex like 01, 12, 012, 1234 etc
        return ','.join([str(i) + ":" + str(self.degree) for i in self.kvertices])

    def __eq__(self, other):
        '''
        Check whether two k-simplex are the same irrespective of the orientation
        :param other: Another KSimplex
        :return: true if both simplex are same or may be just different orientation
        '''
        if self.k == other.k:
            return sorted(self.kvertices) == sorted(other.kvertices)
        return False

    def isEmpty(self):
        return self.k < 0

    def hasVertex(self, v):
        assert isinstance(v, int)
        return v in self.kvertices

class SimplicialComplex:
    def __init__(self):
        self.simplex = []  # Stores all the simplices in the complex
        self.tableofksimplex = {}  # key = k , value = list of k-simplices in the simplicial_complex
        self.maxK = 0  # Keep track of highest Dimensional simplex in the complex

    def get_allkth_simplices(self, k):
        return sorted([obj for obj in self.tableofksimplex.get(k, [])], key=lambda ob: ob.id)

    def add_simplex_fromfile(self, filename):
        '''
        Takes filename as input stream for simplices
        :param filename:
        :return:
        '''
        with open(filename, 'r') as fp:
            while 1:
                line = fp.readline()
                if not line:
                    break
                ksimplex_obj = KSimplex(sorted([int(v) for v in
                                                line.split()]))  # Building the K-simplex object . Always insert them in sorted order to avoid orientation conflict between higher dimensional simplices.
                self.add_simplex(ksimplex_obj)

    def add_simplex(self, ksimplex):
        '''
        Add a k-simplex to the simplicial complex. Can be added in any order and any dimension.
        :param ksimplex:
        :return: None
        '''
        assert isinstance(ksimplex, KSimplex)
        self.simplex.append(ksimplex)
        if self.tableofksimplex.get(ksimplex.k, None) is None:
            self.tableofksimplex[ksimplex.k] = []
        self.tableofksimplex[ksimplex.k].append(ksimplex)

        self.maxK = [self.maxK, ksimplex.k][
            ksimplex.k > self.maxK]  # update maxK if a higher dimensional simplex is added

    def __str__(self):
        toreturn = ''
        for k, simplices in self.tableofksimplex.items():
            toreturn += str(k) + ': ' + str([str(x) for x in simplices]) + ' '
            toreturn += '\n'
        return toreturn

    def __len__(self):
        return len(self.simplex)
