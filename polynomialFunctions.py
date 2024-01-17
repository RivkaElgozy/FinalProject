import matplotlib.pyplot as plt
import random
import keyboard
import multiprocessing
import sympy
from polyClassTest import *


# def get_prime_number():
#     while True:
#         p = input("Enter a prime number: ")
#         if p.isdigit():
#             p = int(p)
#             if sympy.isprime(p):
#                 break
#             else:
#                 print("The number is not prime. Please enter a prime number.")
#         else:
#             print("Invalid input, Please enter a prime number.")
#     return p


def get_prime_number(entry, result_label):
    p = entry.get()
    if p.isdigit():
        p = int(p)
        if sympy.isprime(p):
            result_label.config(text="The number is prime.")
        else:
            result_label.config(text="The number is not prime. Please enter a prime number.")
    else:
        result_label.config(text="Invalid input. Please enter a prime number.")
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
    difference = coordinate_first_point.subtract(coordinate_second_point, False)
    poly_mul = z.multiply(difference)
    remainder = poly_mul.divide(Poly(field_p.irreduciblePolynomial, field_p))[1]
    coordinate = remainder.add(coordinate_second_point, False)
    return coordinate


def process_combination_wrapper(args):
    return get_intersections_parallel(*args)


def get_intersections_parallel(a, b, field_p, hash_table):
    linear_line_points = get_linear_line_between_2_points(a, b, field_p)
    return matches_counter(linear_line_points, hash_table)


def stop_computation():
    global stop_flag
    stop_flag = True


def get_number_of_intersections_list_parallel(graph_points, field_p, window):
    counter_values = []
    hash_table = create_hash_table(graph_points)
    selected_indexes = set()
    combinations = []

    button_stop = tk.Button(window, text="Stop", command=stop_computation)
    button_stop.pack(pady=10)

    for i in range(len(graph_points)):
        for j in range(len(graph_points)):
            if i != j and (i, j) not in selected_indexes and (j, i) not in selected_indexes:
                combinations.append((graph_points[i], graph_points[j], field_p, hash_table))
                selected_indexes.add((i, j))

    random.shuffle(combinations)
    global stop_flag
    stop_flag = False
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for result in pool.imap_unordered(process_combination_wrapper, combinations):
            counter_values.append(result)

            # Check for the space key to stop the loop
            # if keyboard.is_pressed('#'):
            if stop_flag:
                pool.terminate()
                break

    return counter_values


# def create_histogram(values, p, graph):
#     # Create a histogram of integer counter values
#     unique_counters = list(set(values))  # Get unique counter values
#     unique_counters.append(min(unique_counters) - 1)
#     unique_counters.append(max(unique_counters) + 1)
#     unique_counters.sort()  # Sort the unique counter values
#
#     # Create a histogram with integer counter values
#     plt.hist(values, bins=unique_counters, align='left', rwidth=0.8)
#     plt.xlabel('Intersections')
#     plt.ylabel('Linear Lines')
#     plt.xticks(unique_counters)  # Set x-axis ticks to unique counters
#     plt.title(f'Histogram for p = {p}')
#     explanation_text = f'This graph has {len(graph.graph_points)} points. The histogram shows the results for {len(values)} lines'
#     plt.text(0.5, 0.95, explanation_text, transform=plt.gca().transAxes, ha='center', va='center',
#              bbox=dict(facecolor='white', alpha=0.5))
#
#     plt.show()


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
        return Poly([0, int(node.value)], field_p)
    if node.value.lower() == 'x':
        return x
    elif node.value.lower() == 'y':
        return y
    elif node.value.lower() == 'p':
        return Poly([0, field_p.p], field_p)
    elif node.value == '^':
        left_result = evaluate_tree_node(node.left, x, y, field_p, True)
        right_result = evaluate_tree_node(node.right, x, y, field_p, True)
        return left_result.pow(right_result.coefficients[1])
    elif node.value in ['+', '-', '*', '/']:
        left_result = evaluate_tree_node(node.left, x, y, field_p, False)
        right_result = evaluate_tree_node(node.right, x, y, field_p, False)
        if node.value == '+':
            return left_result.add(right_result, flag)
        elif node.value == '-':
            return left_result.subtract(right_result, flag)
        elif node.value == '*':
            return left_result.multiply(right_result)
        elif node.value == '/':
            if right_result.coefficients == [0] or right_result.coefficients == [0, 0]:
                return
            return left_result.divide(right_result)[0]


import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk


def create_histogram(values, p, graph, window):
    # Create a histogram of integer counter values
    unique_counters = list(set(values))
    unique_counters.append(min(unique_counters) - 1)
    unique_counters.append(max(unique_counters) + 1)
    unique_counters.sort()

    # Create a Matplotlib figure and histogram
    fig = Figure(figsize=(6, 4), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.hist(values, bins=unique_counters, align='left', rwidth=0.8)
    ax.set_xlabel('Intersections')
    ax.set_ylabel('Linear Lines')
    ax.set_xticks(unique_counters)
    ax.set_title(f'Histogram for p = {p}')
    explanation_text = f'This graph has {len(graph.graph_points)} points. The histogram shows the results for {len(values)} lines'
    ax.text(0.5, 0.95, explanation_text, transform=ax.transAxes, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    # Embed the Matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Show the Matplotlib figure
    canvas.draw()
