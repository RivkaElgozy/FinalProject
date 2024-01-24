from polynomialFunctions import *
from GraphPolynomialClass import Graph
from FieldClass import field
import tkinter as tk
import threading
import sympy


def submit_action():
    # Disable the Submit button
    # button_submit.config(state=tk.DISABLED)
    button_submit.pack_forget()

    prime_number = get_prime_number(entry_prime, result_label_prime)
    graph_expression = entry_graph.get()  # Get the user's input for the graph expression

    # Destroy the existing Canvas widget
    for widget in window.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

    if sympy.isprime(prime_number):
        # Start a thread for the heavy computations
        computation_thread = threading.Thread(target=main, args=(prime_number, graph_expression))
        computation_thread.start()

        # Check the thread status periodically and re-enable the Submit button when it finishes
        window.after(100, lambda: check_thread_status(computation_thread))
    else:
        # button_submit.config(state=tk.NORMAL)
        button_submit.pack(pady=10)


def check_thread_status(thread):
    if thread.is_alive():
        # If the thread is still running, check again after 100 milliseconds
        window.after(100, lambda: check_thread_status(thread))
    else:
        for widget in window.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Stop":
                widget.destroy()
        # If the thread has finished, enable the Submit button
        # button_submit.config(state=tk.NORMAL)
        # button_submit.pack()


def main(p, graph_expression):
    # The heavy computations inside your main function
    field_p = field(p, None)
    graph_polynomial = Graph(field_p, graph_expression)
    if graph_polynomial.graph_points:
        create_histogram(get_number_of_intersections_list_parallel(graph_polynomial.graph_points, field_p, window), field_p.p, graph_polynomial, window, button_submit)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Prime Number Input Screen")
    window.geometry("800x600")

    # Create and place input widgets
    label_prime = tk.Label(window, text="Enter a prime number:")
    label_prime.pack(pady=10)

    entry_prime = tk.Entry(window)
    entry_prime.pack(pady=10)

    result_label_prime = tk.Label(window, text="")
    result_label_prime.pack(pady=10)

    label_graph = tk.Label(window, text="Enter the graph expression:")
    label_graph.pack(pady=10)

    entry_graph = tk.Entry(window, width=30)
    entry_graph.pack(pady=10)
    entry_graph.insert(0, "x^p + x = y^(p+1)")  # Set default value , (x^p + x)*(y^(p-1)+1) = y^(p) - GS Graph

    button_submit = tk.Button(window, text="Submit", command=submit_action)
    button_submit.pack(pady=10)

    # Start the GUI event loop
    window.mainloop()
