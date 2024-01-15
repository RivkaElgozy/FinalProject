from binaryTree import equation_to_binary_tree
from polynomialFunctions import *
from polyClassTest import *
import time



class Graph:
    def __init__(self, field_p, graph):
        self.graph = graph
        self.field_p = field_p
        self.graph_points = self.calc_graph_points()

    def validate_parentheses(self):
        stack = []
        for char in self.graph:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    print("Mismatched parentheses in the graph expression.")
                    return False
                stack.pop()

        if stack:
            print("Mismatched parentheses in the graph expression.")
            return False
        return True

    def calc_graph_points(self):
        primeNumber = self.field_p.p
        # Validate parentheses
        # Validate parentheses
        if not self.validate_parentheses():
            return False

        # Split the graph expression into individual components
        components = self.graph.split('=')
        if len(components) != 2:
            raise ValueError("Invalid graph expression format. It should be of the form 'expression = expression'.")

        graph_points = []
        leftSide, rightSide = components
        leftTree = equation_to_binary_tree(leftSide)
        rightTree = equation_to_binary_tree(rightSide)
        for a in range(primeNumber):
            for b in range(primeNumber):
                # x = Poly([a, b], field(primeNumber))
                x = Poly([a, b], self.field_p)
                for c in range(primeNumber):
                    for d in range(primeNumber):
                        # y = Poly([c, d], field(primeNumber))
                        y = Poly([c, d], self.field_p)
                        # print("x: ", x)
                        # print("y: ", y)
                        # Parse and evaluate the expressions
                        leftSide_poly = evaluate_tree_node(leftTree, x, y, self.field_p, False)
                        rightSide_poly = evaluate_tree_node(rightTree, x, y, self.field_p, False)
                        # print("leftSide_poly: ", leftSide_poly)
                        # print("rightSide_poly: ", rightSide_poly)
                        # Check if the pair satisfies the equation
                        if str(leftSide_poly) == str(rightSide_poly):
                            graph_points.append((x, y))
        return graph_points


    def print_graph_points(self):
        print("The Graph points:")
        for coordinate_a, coordinate_b in self.graph_points:
            print(f"coordinate_a = {coordinate_a}, coordinate_b = {coordinate_b}")

