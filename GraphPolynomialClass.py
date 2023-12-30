from polynomial import Polynomial
from PolyClass import poly
from binaryTree import equation_to_binary_tree
from polynomialFunctions import *


class Graph:
    def __init__(self, field_p, graph):
        self.graph = graph
        self.field_p = field_p
        self.graph_points = self.calc_graph_points()

    def calc_graph_points(self):#calculate
        primeNumber = self.field_p.p
        # Validate parentheses
        if self.graph.count('(') != self.graph.count(')'):
            raise ValueError("Mismatched parentheses in the graph expression.")

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
                x = poly([a, b])
                for c in range(primeNumber):
                    for d in range(primeNumber):
                        y = poly([a, b])
                        # Parse and evaluate the expressions
                        leftSide_poly = evaluate_tree_node(leftTree, x, y, primeNumber, self.field_p.irreduciblePolynomial)
                        rightSide_poly = evaluate_tree_node(rightTree, x, y, primeNumber, self.field_p.irreduciblePolynomial)

                        # Check if the pair satisfies the equation
                        if leftSide_poly == rightSide_poly:
                            graph_points.append((x, y))

        return graph_points


    def print_graph_points(self):
        print("The Graph points:")
        for coordinate_a, coordinate_b in self.graph_points:
            print(f"coordinate_a = {coordinate_a}, coordinate_b = {coordinate_b}")

