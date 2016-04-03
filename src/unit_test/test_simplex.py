from __future__ import absolute_import
from src.simplex import KSimplex, SimplicialComplex
from src.Filtration import Filtration
from src.boundaryoperator import Boundary
from src.ReductionAlgorithm import StandardMatrix
import copy
from src.ComputeInterval import IntervalComputation

def test_manual_simplex():
    sim = KSimplex([1, 2, 3])
    C = SimplicialComplex()
    C.add_simplex(sim)
    for i in range(2):
        sim = KSimplex(range(i + 1))
        C.add_simplex(sim)
    C.add_simplex(KSimplex([2, 3]))
    print C


def test_file_simplex():
    sigma = SimplicialComplex()
    sigma.add_simplex_fromfile('test_simplexfromfile.txt')
    print sigma


def test_boundary_op():
    delta = Boundary()
    delta.compute_boundary(KSimplex([1, 2, 3]))
    print delta


def test_nested_boundary():
    delta_k = Boundary()
    delta_k.compute_boundary(KSimplex([1, 2, 3]))
    print delta_k
    for sign, kmin1_simpl in delta_k.get_boundary():
        # print kmin1_simpl.k
        delta_kmin1 = Boundary()
        delta_kmin1.compute_boundary(kmin1_simpl)
        print delta_kmin1


def test_nested_boundary_simplicialcomplex():
    sigma = SimplicialComplex()
    sigma.add_simplex_fromfile('test_simplexfromfile.txt')

    for k in range(sigma.maxK + 1):
        print str(k) + '-th Chain group:'
        for k_sim in sigma.get_allkth_simplices(k):
            delta_k = Boundary()
            delta_k.compute_boundary(k_sim)
            print 'Boundary of: ', str(k_sim), ': ', str(delta_k)


def test_manual_Filtration():
    fil = Filtration()
    fil.add_simplex_toith_filtration(0, [0])
    fil.add_simplex_toith_filtration(0, [1])
    fil.add_simplex_toith_filtration(1, [2])
    fil.add_simplex_toith_filtration(1, [3])
    fil.add_simplex_toith_filtration(1, [0, 1])
    fil.add_simplex_toith_filtration(1, [1, 2])  # The simplices should be sorted
    fil.add_simplex_toith_filtration(2, [0, 2])
    print fil
    # print [str(sigma)+" id: "+ str(sigma.id)  for sigma in fil.get_ksimplices_from_ithFiltration(0,0)]

def test_File_Filtration():
    fil = Filtration()
    fil.add_simplices_from_file('../../data/test_simplexfromfile.txt')
    # for i in range(3):
    #    print str(fil.get_ithfiltration(i))


    Mk = StandardMatrix(fil, 1)
    Mk_plusone = StandardMatrix(fil, 2)
    mkhat, mkplusonehat = Mk.get_reduced_matrices(Mk_plusone.get_transpose())

    for p in mkhat:
        print str(p)
    for p in mkplusonehat:
        print str(p)


def test_persistencehomology():
    fil = Filtration()
    # name = "/Users/naheed/NetBeansProjects/Toy-1"
    # name = "/Users/naheed/NetBeansProjects/jplex_explore/3437-1"
    # name = "/Users/naheed/NetBeansProjects/Toy-2 262143"
    # name = "/Users/naheed/NetBeansProjects/Toy-3 2047 (11 Vertex Big Cylce)"
    # fil.add_simplices_from_cliquefiles(name)

    fil.add_simplices_from_file('../../data/test_simplexfromfile.txt')
    # TO DO: Implement the papers version here.
    ci = IntervalComputation(fil)
    ci.compute_intervals(2)
    ci.print_BettiNumbers()
    ci.get_representativs()
    #print ci.betti_intervals

if __name__ == "__main__":
    # test_File_Filtration()
    test_persistencehomology()
    #test_manual_Filtration()
    # test_manual_simplex()
    # test_file_simplex()
    # test_boundary_op()
    # test_nested_boundary()
    # test_nested_boundary_simplicialcomplex()
    # test_kth_boundary_group()
