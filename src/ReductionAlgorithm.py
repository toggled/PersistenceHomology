__author__ = 'Naheed'
import numpy as np
from src.boundaryoperator import *
from src.simplex import *
from src.Filtration import Filtration
from os import sys
import copy
from sympy import Symbol

"""
NingNing's version of the Algorithm (
"""
class vector_of_polynomials:
    def __init__(self, dim, exps, coeffs):
        """
        :rtype: vector_of_polynomials
        """
        self.dim = dim
        self.exponents = exps
        self.coefficients = coeffs

    def __str__(self):
        return ' '.join([str(c) + '*t^' + str(e) for c, e in zip(self.coefficients, self.exponents)])

    def get_lift_degree(self, deg):
        exp_list = [i + deg for i in self.exponents]
        coeffs = self.coefficients
        return vector_of_polynomials(self.dim, exp_list, coeffs)

    def add(self, vect_pol):
        assert isinstance(vect_pol, vector_of_polynomials)
        for i in range(vect_pol.dim):
            if self.coefficients[i] == 0:
                self.exponents[i] = vect_pol.exponents[i]
            self.coefficients[i] = (self.coefficients[i] + vect_pol.coefficients[i]) % 2  # modulo 2

    def is_nonzero(self, row):
        return self.coefficients[row] == 1

    def is_zeropoly(self):
        return self.coefficients == [0] * len(self.coefficients)

    def get_degree(self, row):
        return self.exponents[row]


class StandardMatrix:
    '''
    Build the Standard Matrix Representation M_k of k-th filtration
    '''

    def __init__(self, filtration, k):
        '''
        :param filtration: Filtration object
        :param k: parameter k for M_k
        :return: None
        '''
        # self.transformation_matrix = self.transformation_matrix = np.zeros((self.uniqueid, len(self.kplus1_simplices)), dtype=np.int32)
        self.std_matrix = []
        self.domain_dk = []  # Ck
        self.range_dk = []  # Ck-1
        self.rangesim_rowidx = {}
        self.std_matrix_transpose = []
        reducedflag = False
        self.interval = {}

        rowid = 0
        for i in range(len(filtration.listof_iFiltration)):
            for ksimplex in filtration.get_ksimplices_from_ithFiltration(k, i):
                if ksimplex:
                    self.domain_dk.append(ksimplex)
            for ksimplex in filtration.get_ksimplices_from_ithFiltration(k - 1, i):
                if ksimplex:
                    self.range_dk.append(ksimplex)
                    self.rangesim_rowidx[tuple(ksimplex.kvertices)] = rowid
                    rowid += 1
        print self.rangesim_rowidx

        # print [str(simp) for simp in self.domain_dk]
        # print [str(simp) for simp in self.range_dk]

        for idx, simp in enumerate(self.domain_dk):
            assert isinstance(simp, KSimplex)
            exps = [0] * len(self.range_dk)
            coefs = [0] * len(self.range_dk)
            boundary = Boundary()
            for sigma_range in boundary.compute_boundary(simp):
                thesimplex = sigma_range[1]
                if thesimplex.isEmpty():
                    break
                indx = self.rangesim_rowidx[tuple(thesimplex.kvertices)]
                coefs[indx] = sigma_range[0]  # 1 basically
                # The difference in their degree will be exponent
                exps[indx] = simp.degree - filtration.simplex_to_filtrationmap[tuple(thesimplex.kvertices)]

            # print coefs,exps,str(simp)

            self.std_matrix.append(vector_of_polynomials(len(exps), exps, coefs))
        self.print_stdmatrix()

    def get_dimension(self):
        return (len(self.range_dk), len(self.domain_dk))

    def get_transpose(self):
        exps = [[0 for x in self.domain_dk] for y in self.range_dk]
        coefs = [[0 for x in self.domain_dk] for y in self.range_dk]
        for col in range(len(self.domain_dk)):
            for row in range(len(self.range_dk)):
                exps[row][col] = self.std_matrix[col].exponents[row]
                coefs[row][col] = self.std_matrix[col].coefficients[row]

        for row in range(len(self.range_dk)):
            self.std_matrix_transpose.append(vector_of_polynomials(len(self.range_dk), exps[row], coefs[row]))
        return self.std_matrix_transpose

    def print_stdmatrix(self):
        print 'Ck: ', [str(simp) for simp in self.domain_dk]
        print 'Ck-1: ', [str(simp) for simp in self.range_dk]

        for p in self.std_matrix:
            print str(p)

    def get_reduced_matrices(self, delta_kplusone):
        '''
        :param delta_kplusone: M_k+1 Matrix
        :return: self.std_matrix and M_k+1 Matrix in reduced Form
        '''
        assert isinstance(delta_kplusone, list)

        def colSwap(A, i, j):
            A[i], A[j] = A[j], A[i]

        def colCombine(A, addTo, scaleCol, scaleAmt):
            scalar_multiple = A[scaleCol].get_lift_degree(scaleAmt)
            A[addTo].add(scalar_multiple)

        print 'inside simultaneous reduce\n'

        numRows, numCols = self.get_dimension()
        # print numRows,numCols
        i, j = 0, 0
        operation = 1

        while True:
            if i >= numRows or j >= numCols:
                break

            if not self.std_matrix[j].is_nonzero(i):  # Not Pivot Row = causes infinity
                nonzeroCol = j
                while nonzeroCol < numCols:
                    if not self.std_matrix[nonzeroCol].is_nonzero(i):
                        nonzeroCol += 1


                if nonzeroCol == numCols:
                    i += 1
                    continue

                colSwap(self.std_matrix, j, nonzeroCol)
                # We need to swap corresponding rows in Mk+1 as well
                colSwap(delta_kplusone, j, nonzeroCol)
                print 'operation: ', str(operation), '\n'


            else:  # Pivot Row

                pivotcolumn = j
                pivotrow = i
                '''
                print pivotrow,pivotcolumn
                print self.std_matrix[pivotcolumn]
                print self.std_matrix[pivotcolumn].get_degree(pivotrow)
                print self.domain_dk[pivotcolumn],'->',self.domain_dk[pivotcolumn].degree
                print self.range_dk[pivotrow].degree
                '''

                self.interval[tuple(self.range_dk[pivotrow].kvertices)] = (
                self.range_dk[pivotrow].degree, self.domain_dk[pivotcolumn].degree)

            for otherCol in range(j + 1, numCols):
                if self.std_matrix[otherCol].is_nonzero(i):
                    scaleAmt = self.std_matrix[otherCol].get_degree(i) - self.std_matrix[j].get_degree(i)
                    # print scaleAmt
                    colCombine(self.std_matrix, otherCol, j, scaleAmt)

                    # self.print_stdmatrix()
            # self.print_stdmatrix()

            i += 1
            j += 1
        print 'exiting simultaneous reduce\n'

        for col in range(numCols):
            if not self.std_matrix[col].is_zeropoly():
                del delta_kplusone[0]
            else:
                self.domain_dk[tuple(self.domain_dk[col].kvertices)] = (self.domain_dk[col].degree, 'INFINITY')

        reducedflag = True
        return self.std_matrix, delta_kplusone
