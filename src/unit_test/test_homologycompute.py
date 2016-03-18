__author__ = 'Naheed'
from src.simplex import KSimplex, SimplicialComplex
from src.BoundaryGroup import KthBoundaryGroup
from src.homology import another_bettinum, bettiNumber
from HomologyGroup import Homology

if __name__ == '__main__':
    FilePath = "../../data/simplices.out"
    # FilePath = "../../data/test_simplexfromfile.txt"

    sigma = SimplicialComplex()
    sigma.add_simplex_fromfile(FilePath)

    # for k in range(sigma.maxK):  # not maxK + 1
    for k in range(-1, sigma.maxK+1):  # not maxK
        # print str(k + 1) + '-th Transformation Matrix:'
        Bk = KthBoundaryGroup(k)
        Bk.construct_from_simplex(sigma.get_allkth_simplices(k + 1), sigma.simplex_idmap,
                                  sigma.get_allkth_simplices(k))  # Send all the k+1 simplices to it
        # print Bk.get_transformation_matrix()
        # print Bk.get_columnobjects()
        # print Bk.get_rowobjects()
        m = k + 1
        # print str(m + 1) + '-th Transformation Matrix:'
        Bk1 = KthBoundaryGroup(m)
        Bk1.construct_from_simplex(sigma.get_allkth_simplices(m + 1), sigma.simplex_idmap,
                                   sigma.get_allkth_simplices(m))  # Send all the k+1 simplices to it
        # print Bk1.get_transformation_matrix()
        #
        # print Bk1.get_columnobjects()
        # print Bk1.get_rowobjects()
        homology_obj = Homology(Bk, Bk1)
        print 'H', str(k + 1), ' = ', str(homology_obj.compute_betti_number())
        kth_hom_group = homology_obj.compute_kth_homology_groups()
        print kth_hom_group

        # print 'H', str(k + 1), ' = ', bettiNumber(Bk.get_transformation_matrix(), Bk1.get_transformation_matrix())
        # print 'H', str(k + 1), ' = ', another_bettinum(Bk.get_transformation_matrix(), Bk1.get_transformation_matrix())
        # if result == 0:  # if K-th Betti number is 0. the rest will be so
        #break
