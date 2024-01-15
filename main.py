import cProfile
from polynomialFunctions import *
from GraphPolynomialClass import Graph
from FieldClass import field
import tkinter as tk


def submit_action():
    prime_number = get_prime_number(entry, result_label)
    if sympy.isprime(prime_number):
        main(prime_number)
    else:
        get_prime_number(entry, result_label)


def main(p):
    # p = get_prime_number()
    field_p = field(p, None)
    print(f"Irreducible polynomial: ", Poly(field_p.irreduciblePolynomial, field_p))
    graphPolynomial = Graph(field_p, "x^p + x = y^(p+1)")
    # graphPolynomial = Graph(field_p, "(x^p + x)*(y^(p-1)+1) = y^(p)")  # - new akuma GS
    if graphPolynomial.graph_points:
        graphPolynomial.print_graph_points()
        create_histogram(get_number_of_intersections_list_parallel(graphPolynomial.graph_points, field_p), field_p.p, graphPolynomial)

if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Prime Number Input Screen")

    # Create and place input widgets
    label = tk.Label(window, text="Enter a prime number:")
    label.pack(pady=10)

    entry = tk.Entry(window)
    entry.pack(pady=10)

    button = tk.Button(window, text="Submit", command=submit_action)
    button.pack(pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    # Start the GUI event loop
    window.mainloop()
    # main()
    #cProfile.run('main()', sort='cumulative')
