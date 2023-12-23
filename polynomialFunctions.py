import math
from polynomial import Polynomial
import sympy
import matplotlib.pyplot as plt
import random
import keyboard


def get_prime_number():
    while True:
        p = int(input("Enter a prime number: "))
        if sympy.isprime(p):
            break
        else:
            print("The number is not prime. Please enter a prime number.")
    return p


def get_irreducible_polynomial(p):
    x = sympy.Symbol('x')
    for a in range(1, p):
        for b in range(p):
            for c in range(p):
                poly = sympy.Poly(a * x ** 2 + b * x + c, x)
                if not any(poly.subs(x, i) % p == 0 for i in range(p)):
                    print(f"Irreducible polynomial: {poly.as_expr()}")
                    return poly.all_coeffs()
    return None


def get_graph_points(p, coeffs_irreducible_poly):
    graph_points = []
    for a in range(p):
        for b in range(p):
            # calculate w^p+w:
            coordinate_a = Polynomial(a, b)
            coordinate_a_Pow_P_arr = [a] + [0] * (p - 1) + [b]
            coordinate_a_Pow_P = Polynomial(coordinate_a_Pow_P_arr)
            remainder_coordinate_a = divmod(coordinate_a_Pow_P, Polynomial(coeffs_irreducible_poly))[1]
            remainder_coordinate_a = remainder_coordinate_a + coordinate_a
            remainder_coordinate_a_mod_p = get_poly_modP(p, remainder_coordinate_a)
            for c in range(p):
                for d in range(p):
                    # calculate t^(p+1):
                    coordinate_b = Polynomial(c, d)
                    coordinate_b_Pow_P_arr = [c] + [0] * (p - 1) + [d]
                    coordinate_b_Pow_P = Polynomial(coordinate_b_Pow_P_arr)
                    remainder_coordinate_b = divmod(coordinate_b_Pow_P, Polynomial(coeffs_irreducible_poly))[1]
                    remainder_coordinate_b = divmod(coordinate_b * remainder_coordinate_b, Polynomial(coeffs_irreducible_poly))[1]
                    remainder_coordinate_b_mod_p = get_poly_modP(p, remainder_coordinate_b)
                    if Polynomial(remainder_coordinate_a_mod_p) == Polynomial(remainder_coordinate_b_mod_p):
                        graph_points.append((coordinate_a, coordinate_b))
    print("Number of points in the graph: " + str(len(graph_points)))
    return graph_points


def print_graph_points(graph_points):
    print("The Graph points:")
    for coordinate_a, coordinate_b in graph_points:
        print(f"coordinate_a = {coordinate_a}, coordinate_b = {coordinate_b}")


def get_linear_line_between_2_points(first_point, second_point, p, coeffs_irreducible_poly):
    linear_line_points = []
    for z1 in range(p):
        for z2 in range(p):
            z = Polynomial(z1, z2)

            coordinate_a = calculate_coordinate_of_linear_line(p,z,coeffs_irreducible_poly,first_point[0],second_point[0])
            coordinate_b = calculate_coordinate_of_linear_line(p,z,coeffs_irreducible_poly,first_point[1],second_point[1])

            linear_line_points.append((coordinate_a, coordinate_b))
    return linear_line_points

def calculate_coordinate_of_linear_line(p, z, coeffs_irreducible_poly, coordinate_first_point,coordinate_second_point):
    # Gets 2 coordinates respectively and returns the corresponding coordinate in the linear line
    difference = coordinate_first_point - coordinate_second_point
    difference_mod_p = get_poly_modP(p, difference)
    remainder = divmod(z * difference_mod_p, Polynomial(coeffs_irreducible_poly))[1]
    coordinate = remainder + coordinate_second_point
    return get_poly_modP(p, coordinate)

def get_poly_modP(p, polynomial):
    return Polynomial([elem % p for elem in polynomial[:]][::-1])


def get_number_of_intersections_list(graph_points, p, coeffs_irreducible_poly):
    values = []  # List to store counter values
    hash_table = create_hash_table(graph_points)
    selected_indexes = set()

    try:
        while not keyboard.is_pressed(' ') and not len(selected_indexes) == (len(graph_points) * (len(graph_points) - 1)):
            a, b = random.sample(range(len(graph_points)), 2)

            if not ((a, b) in selected_indexes or (b, a) in selected_indexes):
                linear_line_points = get_linear_line_between_2_points(graph_points[a], graph_points[b], p,
                                                                      coeffs_irreducible_poly)
                values.append(matches_counter(linear_line_points, hash_table))

            selected_indexes.add((a, b))

    except KeyboardInterrupt:
        pass

    return values

def create_histogram(values):
    # Create a histogram of integer counter values
    unique_counters = list(set(values))  # Get unique counter values
    unique_counters.append(min(unique_counters) - 1)
    unique_counters.append(max(unique_counters) + 1)
    unique_counters.sort()  # Sort the unique counter values

    # Create a histogram with integer counter values
    plt.hist(values, bins=unique_counters, align='left', rwidth=0.8)
    plt.xlabel('Intersections')
    plt.ylabel('Linear Lines')
    plt.xticks(unique_counters)  # Set x-axis ticks to unique counters
    plt.title('Histogram')
    plt.show()


def create_hash_table(graph_points):
    hash_table = {}
    for point_a, point_b in graph_points:
        key = (f"{point_a}", f"{point_b}")
        hash_table[key] = True
    return hash_table


def matches_counter(linear_line_points, hash_table):
    count = 0
    for point_a,point_b in linear_line_points:
        try:
            key = (f"{point_a}", f"{point_b}")
            if hash_table[key]:
                count += 1
        except KeyError:
            pass  # Key doesn't exist, continue without incrementing count
    return count
