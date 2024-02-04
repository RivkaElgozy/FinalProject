import random
import multiprocessing
import threading

import matplotlib
from matplotlib import pyplot as plt
from polyClassTest import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
matplotlib.use('agg')


def get_prime_number(entry, result_label):
    p = entry.get()
    if p.isdigit():
        p = int(p)
        if sympy.isprime(p):
            result_label.config(text="The number is prime", fg="green")
        else:
            result_label.config(text="The number is not prime. Please enter a prime number", fg="red")
    else:
        result_label.config(text="Invalid input. Please enter a prime number", fg="red")
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
    # # Disable the Submit button
    # for widget in wind.winfo_children():
    #     if isinstance(widget, tk.Button) and widget.cget("text") == "Stop":
    #         widget.pack_forget()
    #
    # # Start a thread for the heavy computations
    # computation_thread = threading.Thread(target=set_stop_flag_true)
    # computation_thread.start()


def set_stop_flag_true():
    global stop_flag
    stop_flag = True


def get_number_of_intersections_list_parallel(graph_points, field_p, window):
    global wind
    wind = window
    counter_values = []
    hash_table = create_hash_table(graph_points)
    selected_indexes = set()
    combinations = []

    # Calculate the total number of valid combinations
    total_combinations = 0

    for i in range(len(graph_points)):
        for j in range(len(graph_points)):
            if i != j and (i, j) not in selected_indexes and (j, i) not in selected_indexes:
                combinations.append((graph_points[i], graph_points[j], field_p, hash_table))
                selected_indexes.add((i, j))
                total_combinations += 1

    # Create a determinate progress bar
    if field_p.p > 3:
        progress_bar = ttk.Progressbar(window, mode="determinate", maximum=total_combinations, length=250)
        progress_label = tk.Label(window, text="Calculating Graph's linear lines", padx=10)
        progress_label.pack(pady=10)
        progress_bar.pack(pady=10)
        button_stop = tk.Button(window, text="Stop", command=stop_computation)
        button_stop.pack(pady=10)

    random.shuffle(combinations)
    global stop_flag
    stop_flag = False
    index = 0
    progress_bar_flag = 0
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for result in pool.imap_unordered(process_combination_wrapper, combinations):
            counter_values.append(result)

            # Check for the space key to stop the loop
            if stop_flag:
                # Stop the progress bar
                pool.terminate()
                break

            # Update the determinate progress bar
            index += 1
            progress_bar_flag += 1
            if field_p.p > 3 and field_p.p**4 <= progress_bar_flag:
                progress_bar_flag = 0
                progress_bar["value"] = index
                window.update_idletasks()

    # Hide the progress bar
    if field_p.p > 3:
        progress_label.pack_forget()
        progress_bar.pack_forget()

    return counter_values


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


def create_histogram(values, p, graph, window, button_submit):
    button_submit.pack(pady=10)
    # Create a histogram of integer counter values
    unique_counters = list(set(values))
    unique_counters.extend([min(values) - 1, max(values) + 1])
    unique_counters.sort()

    # Calculate the difference between ticks
    tick_difference = unique_counters[1] - unique_counters[0]

    # Calculate the new ticks with the same difference
    new_ticks = list(range(min(unique_counters), max(unique_counters) + 1, tick_difference))

    # Create a Matplotlib figure and histogram
    fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
    ax.hist(values, bins=new_ticks, align='left', edgecolor='black', rwidth=0.9, color='skyblue')
    ax.set_xlabel('Intersections')
    ax.set_ylabel('Linear Lines')
    ax.set_xticks(new_ticks)
    ax.set_title(f'Histogram for p = {p}')
    explanation_text = f'This graph has {len(graph.graph_points)} points. The histogram shows the results for {len(values)} lines'
    ax.text(0.5, 0.95, explanation_text, transform=ax.transAxes, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    # Embed the Matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Show the Matplotlib figure
    canvas.draw()
