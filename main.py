import cProfile
from polynomialFunctions import *
from GraphPolynomialClass import Graph
from FieldClass import field
import tkinter as tk
import threading
import sympy


def submit_action():
    # Disable the Submit button
    button_submit.config(state=tk.DISABLED)

    prime_number = get_prime_number(entry, result_label)

    # Destroy the existing Canvas widget
    for widget in window.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

    # Start a thread for the heavy computations
    computation_thread = threading.Thread(target=main, args=(prime_number,))
    computation_thread.start()

    # Check the thread status periodically and re-enable the Submit button when it finishes
    window.after(100, check_thread_status, computation_thread)

def check_thread_status(thread):
    if thread.is_alive():
        # If the thread is still running, check again after 100 milliseconds
        window.after(100, check_thread_status, thread)
    else:
        for widget in window.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Stop":
                widget.destroy()
        # If the thread has finished, enable the Submit button
        button_submit.config(state=tk.NORMAL)

def main(p):
    # The heavy computations inside your main function
    field_p = field(p, None)
    print(f"Irreducible polynomial: ", Poly(field_p.irreduciblePolynomial, field_p))
    graphPolynomial = Graph(field_p, "x^p + x = y^(p+1)")
    # graphPolynomial = Graph(field_p, "(x^p + x)*(y^(p-1)+1) = y^(p)")  # - new akuma GS
    if graphPolynomial.graph_points:
        graphPolynomial.print_graph_points()
        create_histogram(get_number_of_intersections_list_parallel(graphPolynomial.graph_points, field_p, window), field_p.p, graphPolynomial, window)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Prime Number Input Screen")
    window.geometry("800x600")

    # Create and place input widgets
    label = tk.Label(window, text="Enter a prime number:")
    label.pack(pady=10)

    entry = tk.Entry(window)
    entry.pack(pady=10)

    button_submit = tk.Button(window, text="Submit", command=submit_action)
    button_submit.pack(pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    # Start the GUI event loop
    window.mainloop()
    # main()
    #cProfile.run('main()', sort='cumulative')
