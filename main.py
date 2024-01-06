from polynomialFunctions import *
from GraphPolynomialClass import Graph
from PolyClass import poly
from FieldClass import field
from binaryTree import *


def main():
    p = get_prime_number()
    field_p = field(p)
    graphPolynomial = Graph(field_p, "x^p + x = y^(p+1)")
    #GraphPolynomial.graph_points = get_graph_points(p, coeffs_irreducible_poly)
    # X^(p) + X = (y^(p))/(y^(p-1)+1) - new akuma
    graphPolynomial.print_graph_points()
    create_histogram(get_number_of_intersections_list_Parallel(graphPolynomial.graph_points,field_p), field_p.p)

if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort='cumulative')
