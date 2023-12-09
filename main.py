from polynomialFunctions import *
def main():
    p = get_prime_number()
    coeffs_irreducible_poly = get_irreducible_polynomial(p)
    graph_points = get_graph_points(p, coeffs_irreducible_poly)
    # X^(p) + x = (y^(p))/(y^(p-1)+1)
    print_graph_points(graph_points)
    create_histogram(get_intersections_list(graph_points, p, coeffs_irreducible_poly))

if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort='cumulative')
