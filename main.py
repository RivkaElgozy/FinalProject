import cProfile

from polynomialFunctions import *
from GraphPolynomialClass import Graph
from FieldClass import field
from binaryTree import *


def main():
    p = get_prime_number()
    field_p = field(p)
    print(f"Irreducible polynomial: ", Poly(field_p.irreduciblePolynomial, field_p))
    #graphPolynomial = Graph(field_p, "x^p + x = y^(p+1)")
    graphPolynomial = Graph(field_p, "x^p + x = y^(p)/(y^(p-1)+1)")  # - new akuma GS
    if graphPolynomial.graph_points:
        graphPolynomial.print_graph_points()
        create_histogram(get_number_of_intersections_list_parallel(graphPolynomial.graph_points, field_p), field_p.p, graphPolynomial)

if __name__ == "__main__":
    main()
    #cProfile.run('main()', sort='cumulative')
