from polynomialFunctions import *
from GraphPolynomialClass import Graph
from PolyClass import poly
from FieldClass import field
from binaryTree import *


def main():
    p = get_prime_number()
    field_p = field(p)
    print(f"Irreducible polynomial: ", Poly(field_p.irreduciblePolynomial, field_p))
    graphPolynomial = Graph(field_p, "x^p + x = y^(p+1)")
    # graphPolynomial = Graph(field_p, "x^p + x = y^(p)/(y^(p-1)+1)")- new akuma
    if graphPolynomial.graph_points:
        graphPolynomial.print_graph_points()
        create_histogram(get_number_of_intersections_list_Parallel(graphPolynomial.graph_points, field_p), field_p.p)

if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort='cumulative')
