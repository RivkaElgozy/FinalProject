import cProfile
from binaryTree import equation_to_binary_tree
from polynomialFunctions import *
from polyClass import *


class Graph:
    def __init__(self, field_p, graph, window, result_label_graph):
        self.graph = graph.replace(" ", "")
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

    def more_validation(self, result_label_graph, side):

        stack = []
        last_char = None
        has_equals = False

        for char in side:
            if char == '(':
                if last_char and (last_char.isalnum() or last_char == ')'):
                    result_label_graph.config(text="Invalid expression between parentheses", fg="red")
                    return False
                stack.append(char)
            elif char == ')':
                if not stack:
                    result_label_graph.config(text="Mismatched parentheses in the graph expression", fg="red")
                    return False
                stack.pop()
            elif char in '+-*/^':
                if (not last_char or not last_char.isalnum()) and not last_char == ')':
                    result_label_graph.config(text="Invalid expression: Operator cannot come after another operator",
                                              fg="red")
                    return False
            elif char.isalnum():
                if last_char and (last_char.isalnum() or last_char == ')'):
                    result_label_graph.config(
                        text="Invalid expression: Two characters cannot appear consecutively without an operator",
                        fg="red")
                    return False
            elif char == '=':
                if has_equals:
                    result_label_graph.config(text="Invalid expression: '=' can only appear once in the equation",
                                              fg="red")
                    return False
                has_equals = True
                if not last_char or not last_char.isalnum():
                    result_label_graph.config(text="Invalid expression: '=' cannot be preceded by an operator",
                                              fg="red")
                    return False
                if side.index(char) != 0 and not side[side.index(char) - 1].isalnum() and side[
                    side.index(char) - 1] != ')':
                    result_label_graph.config(text="Invalid expression: '=' cannot be preceded by an operator",
                                              fg="red")
                    return False
                if side.index(char) != len(side) - 1 and not side[
                    side.index(char) + 1].isalnum() and side[side.index(char) + 1] != '(':
                    result_label_graph.config(text="Invalid expression: '=' cannot be followed by an operator",
                                              fg="red")
                    return False
            else:
                result_label_graph.config(text="Invalid character in the graph expression", fg="red")
                return False

            last_char = char

        if stack:
            result_label_graph.config(text="Mismatched parentheses in the graph expression", fg="red")
            return False

        if not side[0].isalnum() and side[0] != '(':
            result_label_graph.config(text="Invalid expression: Graph cannot start with an operator or '='", fg="red")
            return False

        if not side[-1].isalnum() and side[-1] != ')':
            result_label_graph.config(text="Invalid expression: Graph cannot end with an operator or '='", fg="red")
            return False

        result_label_graph.config(text="Graph expression is good", fg="green")
        return True

    def calc_graph_points(self, window, result_label_graph):
        prime_number = self.field_p.p
        # Validate parentheses
        if not self.validate_parentheses(result_label_graph):
            return False

        # Split the graph expression into individual components
        components = self.graph.split('=')
        if len(components) != 2:
            result_label_graph.config(text="Invalid graph expression format. It should be of the form 'expression = expression'.",fg="red")            # Split the graph expression into individual components

        try:
            left_side, right_side = components
        except ValueError:
            return False
        if not self.more_validation(result_label_graph, left_side) or not self.more_validation(result_label_graph, right_side):
            return False

        graph_points = []
        left_tree = equation_to_binary_tree(left_side)
        right_tree = equation_to_binary_tree(right_side)
        if prime_number < 5:
            window = None

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
                        left_side_poly = evaluate_tree_node(left_tree, x, y, self.field_p, False)
                        right_side_poly = evaluate_tree_node(right_tree, x, y, self.field_p, False)
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
