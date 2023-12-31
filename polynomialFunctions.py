import math
from polynomial import Polynomial
import sympy
import matplotlib.pyplot as plt
import random
import keyboard
import multiprocessing
from PolyClass import poly



def get_prime_number():
    while True:
        p = int(input("Enter a prime number: "))
        if sympy.isprime(p):
            break
        else:
            print("The number is not prime. Please enter a prime number.")
    return p


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



def get_linear_line_between_2_points(first_point, second_point, field_p):
    linear_line_points = []
    for z1 in range(field_p.p):
        for z2 in range(field_p.p):
            z = Polynomial(z1, z2)

            coordinate_a = calculate_coordinate_of_linear_line(field_p, z,first_point[0],second_point[0])
            coordinate_b = calculate_coordinate_of_linear_line(field_p,z,first_point[1],second_point[1])

            linear_line_points.append((coordinate_a, coordinate_b))
    return linear_line_points

def calculate_coordinate_of_linear_line(field_p, z, coordinate_first_point,coordinate_second_point):
    # Gets 2 coordinates respectively and returns the corresponding coordinate in the linear line
    difference = coordinate_first_point - coordinate_second_point
    difference_mod_p = get_poly_modP(field_p.p, difference)
    remainder = divmod(z * difference_mod_p, Polynomial(field_p.irreduciblePolynomial))[1]
    coordinate = remainder + coordinate_second_point
    return get_poly_modP(field_p.p, coordinate)

def get_poly_modP(p, polynomial):
    return Polynomial([elem % p for elem in polynomial[:]][::-1])


def process_combination_wrapper(args):
    return get_intersections_parallel(*args)


def get_intersections_parallel(a, b, field_p, hash_table):
    linear_line_points = get_linear_line_between_2_points(a, b, field_p)
    return matches_counter(linear_line_points, hash_table)


def get_number_of_intersections_list_Parallel(graph_points, field_p):
    counter_values = []
    hash_table = create_hash_table(graph_points)
    selected_indexes = set()
    combinations = []

    for i in range(len(graph_points)):
        for j in range(len(graph_points)):
            if i != j and (i, j) not in selected_indexes and (j, i) not in selected_indexes:
                combinations.append((graph_points[i], graph_points[j], field_p, hash_table))
                selected_indexes.add((i, j))

    random.shuffle(combinations)
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for result in pool.imap_unordered(process_combination_wrapper, combinations):
            counter_values.append(result)

            # Check for the space key to stop the loop
            if keyboard.is_pressed('#'):
                pool.terminate()
                break

    return counter_values

def create_histogram(values, p):
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
    plt.title(f'Histogram for p = {p}')
    explanation_text = f'This graph has {pow(p, 3)} points. The histogram shows the results for {len(values)} lines'
    plt.text(0.5, 0.95, explanation_text, transform=plt.gca().transAxes, ha='center', va='center',
             bbox=dict(facecolor='white', alpha=0.5))

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


def evaluate_tree_node(node, x, y, field_p):
    print(node.value)
    if node.value.isnumeric():
        return int(node.value)
    if node.value.lower() == 'x':
        if x.coeffs[0] == 0:
            return x.coeffs[1]
        return x
    elif node.value.lower() == 'y':
        if y.coeffs[0] == 0:
            return y.coeffs[1]
        return y
    elif node.value.lower() == 'p':
        return field_p.p
    elif node.value == '^':
        left_result = evaluate_tree_node(node.left, x, y, field_p)
        right_result = int(evaluate_tree_node(node.right, x, y, field_p))
        if isinstance(left_result, int) and isinstance(right_result, int):
            return pow(left_result, right_result) % field_p.p
        return left_result.pow(right_result, field_p)
    elif node.value in ['+', '-', '*', '/']:
        left_result = evaluate_tree_node(node.left, x, y, field_p)
        right_result = evaluate_tree_node(node.right, x, y, field_p)
        if node.value == '+':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return (left_result + right_result) % field_p.p
            return left_result.add_polynomial(field_p.p, right_result)
        elif node.value == '-':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return (left_result - right_result) % field_p.p
            return left_result.sub_polynomial(field_p.p, right_result)
        elif node.value == '*':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return (left_result * right_result) % field_p.p
            return left_result.multiply_polynomial(right_result, field_p)
        elif node.value == '/':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return (left_result / right_result) % field_p.p
            return left_result.divide_polynomial(right_result, field_p)

