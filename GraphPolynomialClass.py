import cProfile
from binaryTree import equation_to_binary_tree
from polynomialFunctions import *
from polyClassTest import *


class Graph:
    def __init__(self, field_p, graph, window, result_label_graph):
        self.graph = graph
        self.field_p = field_p
        self.graph_points = self.calc_graph_points(window, result_label_graph)
        # self.graph_points = self.profile_calc_graph_points(window, result_label_graph)

    def validate_parentheses(self, result_label_graph):
        stack = []
        for char in self.graph:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    result_label_graph.config(text="Mismatched parentheses in the graph expression", fg="red")
                    return False
                stack.pop()

        if stack:
            result_label_graph.config(text="Mismatched parentheses in the graph expression", fg="red")
            return False
        result_label_graph.config(text="Graph expression is good", fg="green")
        return True

    def calc_graph_points(self, window, result_label_graph):
        prime_number = self.field_p.p
        # Validate parentheses
        if not self.validate_parentheses(result_label_graph):
            return False

        if prime_number < 5:
            window = None

        # Split the graph expression into individual components
        components = self.graph.split('=')
        if len(components) != 2:
            raise ValueError("Invalid graph expression format. It should be of the form 'expression = expression'.")

        graph_points = []
        leftSide, rightSide = components
        leftTree = equation_to_binary_tree(leftSide)
        rightTree = equation_to_binary_tree(rightSide)
        if window is not None:
            max_number = prime_number
            # Create a determinate progress bar
            progress_bar = ttk.Progressbar(window, mode="determinate", maximum=max_number, length=250)
            progress_label = tk.Label(window, text="Calculating Graph's points", padx=10)
            progress_label.pack(pady=10)
            progress_bar.pack(pady=10)
        index = 0

        for a in range(prime_number):
            for b in range(prime_number):
                x = Poly([a, b], self.field_p)
                for c in range(prime_number):
                    for d in range(prime_number):
                        y = Poly([c, d], self.field_p)
                        left_side_poly = evaluate_tree_node(leftTree, x, y, self.field_p, False)
                        right_side_poly = evaluate_tree_node(rightTree, x, y, self.field_p, False)
                        if str(left_side_poly) == str(right_side_poly):
                            graph_points.append((x, y))
            # Update the determinate progress bar
            if window is not None:
                index += 1
                progress_bar["value"] = index
                window.update_idletasks()
        # Hide the progress bar
        if window is not None:
            progress_label.pack_forget()
            progress_bar.pack_forget()
        return graph_points

    def profile_calc_graph_points(self, window, result_label_graph):
        profile_results = cProfile.runctx('self.calc_graph_points(None, result_label_graph)', globals(), locals(), sort='cumulative')
        return profile_results

    def print_graph_points(self):
        print("The Graph points:")
        for coordinate_a, coordinate_b in self.graph_points:
            print(f"coordinate_a = {coordinate_a}, coordinate_b = {coordinate_b}")
