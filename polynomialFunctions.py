import matplotlib.pyplot as plt
import random
import keyboard
import multiprocessing
from polyClassTest import *
import math

# Function to find modulo inverse of b. It returns
# -1 when inverse doesn't
# modInverse works for prime m
def modInverse(b,m):
    g = math.gcd(b, m)
    if (g != 1):
        # print("Inverse doesn't exist")
        return -1
    else:
        # If b and m are relatively prime,
        # then modulo inverse is b^(m-2) mode m
        return pow(b, m - 2, m)


# Function to compute a/b under modulo m
def modDivide(a, b, m):
    a = a % m
    inv = modInverse(b, m)
    if inv == -1:
        print("Division not defined")
    else:
        return  (inv*a) % m


def get_prime_number():
    while True:
        p = int(input("Enter a prime number: "))
        if sympy.isprime(p):
            break
        else:
            print("The number is not prime. Please enter a prime number.")
    return p


def get_linear_line_between_2_points(first_point, second_point, field_p):
    linear_line_points = []
    for z1 in range(field_p.p):
        for z2 in range(field_p.p):
            z = Poly([z1, z2], field_p)

            coordinate_a = calculate_coordinate_of_linear_line(field_p, z,first_point[0],second_point[0])
            coordinate_b = calculate_coordinate_of_linear_line(field_p,z,first_point[1],second_point[1])

            linear_line_points.append((coordinate_a, coordinate_b))
    return linear_line_points


def calculate_coordinate_of_linear_line(field_p, z, coordinate_first_point,coordinate_second_point):
    # Gets 2 coordinates respectively and returns the corresponding coordinate in the linear line
    difference = coordinate_first_point.subtract(coordinate_second_point)
    poly_mul = z.multiply(difference)
    remainder = poly_mul.divide(Poly(field_p.irreduciblePolynomial, field_p))[1]
    coordinate = remainder.add(coordinate_second_point)
    return coordinate


def process_combination_wrapper(args):
    return get_intersections_parallel(*args)


def get_intersections_parallel(a, b, field_p, hash_table):
    linear_line_points = get_linear_line_between_2_points(a, b, field_p)
    return matches_counter(linear_line_points, hash_table)


def get_number_of_intersections_list_parallel(graph_points, field_p):
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


def create_histogram(values, p, graph):
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
    explanation_text = f'This graph has {len(graph.graph_points)} points. The histogram shows the results for {len(values)} lines'
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


def evaluate_tree_node(node, x, y, field_p, flag):
    if node.value.isnumeric():
        return int(node.value)
    if node.value.lower() == 'x':
        if x.coefficients[0] == 0:
            try:
                return Poly([0]+[x.coefficients[1]], field_p)
            except:
                return Poly([0], field_p)
        return x
    elif node.value.lower() == 'y':
        if y.coefficients[0] == 0:
            try:
                return y.coefficients[1]
            except:
                return Poly([0], field_p)
        return y
    elif node.value.lower() == 'p':
        return field_p.p
    elif node.value == '^':
        left_result = evaluate_tree_node(node.left, x, y, field_p, True)
        right_result = int(evaluate_tree_node(node.right, x, y, field_p, True))
        if isinstance(left_result, int) and isinstance(right_result, int):
            return pow(left_result, right_result) % field_p.p
        return left_result.pow(right_result)
    elif node.value in ['+', '-', '*', '/']:
        left_result = evaluate_tree_node(node.left, x, y, field_p, False)
        right_result = evaluate_tree_node(node.right, x, y, field_p, False)
        # if not isinstance(left_result, int):
        #     left_result = remove_leading_zeros(left_result.coefficients, left_result.field)
        # if not isinstance(right_result, int):
        #     right_result = remove_leading_zeros(right_result.coefficients, right_result.field)
        if node.value == '+':
            if isinstance(left_result, int) and isinstance(right_result, int):
                if flag:
                    return left_result + right_result
                return (left_result + right_result) % field_p.p
            if isinstance(left_result, int):
                return Poly([left_result], field_p).add(right_result)
            if isinstance(right_result, int):
                return left_result.add(Poly([0, right_result], field_p))
            return left_result.add(right_result)
        elif node.value == '-':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return left_result - right_result
            if isinstance(left_result, int):
                return Poly([0, left_result], field_p).subtract(right_result)
            if isinstance(right_result, int):
                return left_result.subtract(Poly([0, right_result], field_p))
            return left_result.subtract(right_result)
        elif node.value == '*':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return left_result * right_result
            if isinstance(left_result, int):
                return Poly([0, left_result], field_p).multiply(right_result)
            if isinstance(right_result, int):
                return left_result.multiply(Poly([0, right_result], field_p))
            return left_result.multiply(right_result)
        elif node.value == '/':
            if isinstance(left_result, int) and isinstance(right_result, int):
                return modDivide(left_result, right_result, field_p.p)
                #return left_result / right_result
            if isinstance(left_result, int):
                if right_result == 0:
                    return
                return Poly([0, left_result], field_p).divide(right_result)[0]
            if isinstance(right_result, int):
                if left_result == 0:
                    return
                return left_result.divide(Poly([0, right_result], field_p))[0]
            if right_result.coefficients == [0] or right_result.coefficients == [0, 0]:
                return
            return left_result.divide(right_result)[0]

def remove_leading_zeros(arr, field):
    if isinstance(arr, Poly):
        arr = arr.coefficients
    # Find the index of the first non-zero element
    non_zero_index = next((i for i, x in enumerate(arr) if x != 0), None)

    if non_zero_index is not None:
        # Slice the array from the first non-zero element onward
        result = arr[non_zero_index:]
        if len(result) == 1:
            return result[0]
        return Poly(result, field)
    else:
        # If the array is all zeros, return a single-element array with 0
        return 0
