import cProfile

from polynomial import Polynomial
import sympy
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import numba
from numba import jit


# learning polynomial library:
# a = Polynomial(1, 2, 3, 4)
# print(str(a))
# #x^3 + 2x^2 + 3x + 4
#
# p = Polynomial(1, 1) * Polynomial(2, 2)
# print(str(p))
# #2x^2 + 4x + 2
#
# q, remainder = divmod(p, Polynomial(1, 2))
# print(str(remainder))
# #2 --> (2x^2 + 4x + 2) mod (x + 2) = 2


def get_prime():
    while True:
        p = int(input("Enter a prime number: "))
        if sympy.isprime(p):
            break
        else:
            print("The number is not prime. Please enter a prime number.")
    return p


def find_irreducible_poly(p):
    x = sympy.Symbol('x')
    for a in range(1, p):
        for b in range(p):
            for c in range(p):
                poly = sympy.Poly(a * x ** 2 + b * x + c, x)
                if not any(poly.subs(x, i) % p == 0 for i in range(p)):
                    return poly
    return None


def find_polynomials2(p, coeffs_irreducible_poly):
    result = []
    for a in range(p):
        for b in range(p):
            # calculate w^p+w:
            w = Polynomial(a, b)
            arrW = [a] + [0] * (p - 1) + [b]
            wPowP = Polynomial(arrW)
            remainderW = divmod(wPowP, Polynomial(coeffs_irreducible_poly))[1]
            remainderW = remainderW + w
            remainderW_mod_p = [elem % p for elem in remainderW[:]][::-1]
            for c in range(p):
                for d in range(p):
                    # calculate t^(p+1)
                    t = Polynomial(c, d)
                    arrT = [c] + [0] * (p - 1) + [d]
                    tPowP = Polynomial(arrT)
                    remainderT = divmod(tPowP, Polynomial(coeffs_irreducible_poly))[1]
                    remainderT = divmod(t * remainderT, Polynomial(coeffs_irreducible_poly))[1]
                    remainderT_mod_p = [elem % p for elem in remainderT[:]][::-1]
                    if Polynomial(remainderW_mod_p) == Polynomial(remainderT_mod_p):
                        result.append((w, t))
    print("Number of (w,t): " + str(len(result)))
    return result


def printPolyPoints(polynomials1):
    print("Found polynomials w, t that satisfy the equation:")
    for w, t in polynomials1:
        print(f"w = {w}, t = {t}")


def printLinearLine(a, b, p, coeffs_irreducible_poly):
    result = []
    for z1 in range(p):
        for z2 in range(p):
            z = Polynomial(z1, z2)
            w = a[0]
            t = a[1]
            wTag = b[0]
            tTag = b[1]
            # w:
            resW = w - wTag
            remainderW_mod_p = Polynomial([elem % p for elem in resW[:]][::-1])
            remainderW = divmod(z * remainderW_mod_p, Polynomial(coeffs_irreducible_poly))[1]
            res1 = remainderW + wTag
            res1_mod_p = Polynomial([elem % p for elem in res1[:]][::-1])
            # t:
            resT = t - tTag
            remainderT_mod_p = Polynomial([elem % p for elem in resT[:]][::-1])
            remainderT = divmod(z * remainderT_mod_p, Polynomial(coeffs_irreducible_poly))[1]
            res2 = remainderT + tTag
            res2_mod_p = Polynomial([elem % p for elem in res2[:]][::-1])
            result.append((res1_mod_p, res2_mod_p))
    return result




def findLines(polynomials1, p, coeffs_irreducible_poly):
    counter_values = []  # List to store counter values
    hash_table = create_hash_table(polynomials1)
    for a in polynomials1:
        for b in [x for x in polynomials1 if x != a]:
            result = printLinearLine(a, b, p, coeffs_irreducible_poly)
            counter = matches_counter(result, hash_table)
            counter_values.append(counter)
    # result = printLinearLine((Polynomial(1), Polynomial(0)),(Polynomial(1), Polynomial(0)), p, coeffs_irreducible_poly)
    # counter = matches_counter(result, hash_table)
    # counter_values.append(counter)

    # Create a histogram of integer counter values
    unique_counters = list(set(counter_values))  # Get unique counter values
    unique_counters.append(min(unique_counters) - 1)
    unique_counters.append(max(unique_counters) + 1)
    unique_counters.sort()  # Sort the unique counter values

    # Create a histogram with integer counter values
    plt.hist(counter_values, bins=unique_counters, align='left', rwidth=0.8)
    plt.xlabel('Counter')
    plt.ylabel('Frequency')
    plt.xticks(unique_counters)  # Set x-axis ticks to unique counters
    plt.title('Counter Frequency')
    plt.show()


def create_hash_table(polynomials):
    hash_table = {}
    for w,t in polynomials:
        key = (f"{w}", f"{t}")
        hash_table[key] = True

    return hash_table


def matches_counter(result, hash_table):
    count = 0
    for w,t in result:
        try:
            key = (f"{w}", f"{t}")
            if hash_table[key]:
                count += 1
        except KeyError:
            pass  # Key doesn't exist, continue without incrementing count
    return count

import multiprocessing

def process_combination_wrapper(args):
    a, b, p, coeffs_irreducible_poly, hash_table = args
    result = printLinearLine(a, b, p, coeffs_irreducible_poly)
    counter = matches_counter(result, hash_table)
    return counter

def findLinesParallel(polynomials1, p, coeffs_irreducible_poly):
    counter_values = []
    hash_table = create_hash_table(polynomials1)

    # Create a list of argument tuples for each combination of a and b
    combinations = [(a, b, p, coeffs_irreducible_poly, hash_table) for a in polynomials1 for b in polynomials1 if b != a]
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    results = p.map(process_combination_wrapper, combinations)

    # Use multiprocessing to parallelize the work
    # with multiprocessing.Pool() as pool:
    #     results = pool.map(process_combination_wrapper, combinations)

    # Combine the results from different processes
    counter_values.extend(results)

    # Rest of your code remains unchanged
    unique_counters = list(set(counter_values))
    unique_counters.append(min(unique_counters) - 1)
    unique_counters.append(max(unique_counters) + 1)
    unique_counters.sort()

    plt.hist(counter_values, bins=unique_counters, align='left', rwidth=0.8)
    plt.xlabel('Counter')
    plt.ylabel('Frequency')
    plt.xticks(unique_counters)
    plt.title('Counter Frequency')
    plt.show()

    pd.set_option('display.max_rows', None)

# from multiprocessing import Process, Queue, current_process
# import queue
# from multiprocessing import cpu_count
#
# def process_combination_wrapper(tasks_to_accomplish, tasks_that_are_done):
#     while True:
#         try:
#             task = tasks_to_accomplish.get_nowait()
#         except queue.Empty:
#             break
#         else:
#             a, b, p, coeffs_irreducible_poly, hash_table = task
#             result = printLinearLine(a, b, p, coeffs_irreducible_poly)
#             counter = matches_counter(result, hash_table)
#             tasks_that_are_done.put(counter)
#
# def findLinesParallel(tasks_to_accomplish, tasks_that_are_done, polynomials1, p, coeffs_irreducible_poly):
#     number_of_processes = cpu_count()
#     processes = []
#     hash_table = create_hash_table(polynomials1)
#
#     # preparing tasks and starting parallel processing
#     for a in polynomials1:
#         for b in [x for x in polynomials1 if x != a]:
#             tasks_to_accomplish.put((a, b, p, coeffs_irreducible_poly, hash_table))
#
#     # creating processes
#     for _ in range(number_of_processes):
#         p = Process(target=process_combination_wrapper, args=(tasks_to_accomplish, tasks_that_are_done))
#         processes.append(p)
#         p.start()
#
#     # joining processes
#     for p in processes:
#         p.join()


def main():
    p = get_prime()
    irreducible_poly = find_irreducible_poly(p)
    print(f"Irreducible polynomial: {irreducible_poly.as_expr()}")
    coeffs_irreducible_poly = irreducible_poly.all_coeffs()
    polynomials1 = find_polynomials2(p, coeffs_irreducible_poly)
    printPolyPoints(polynomials1)
    #findLines(polynomials1, p, coeffs_irreducible_poly)
    findLinesParallel(polynomials1, p, coeffs_irreducible_poly)
    # tasks_to_accomplish = Queue()
    # tasks_that_are_done = Queue()
    #
    # findLinesParallel(tasks_to_accomplish, tasks_that_are_done, polynomials1, p, coeffs_irreducible_poly)
    # # print the output
    # while not tasks_that_are_done.empty():
    #     #print(tasks_that_are_done.get())
    #     counter_values.append(tasks_that_are_done.get())

    # # Create a histogram of integer counter values
    # unique_counters = list(set(counter_values))  # Get unique counter values
    # unique_counters.append(min(unique_counters) - 1)
    # unique_counters.append(max(unique_counters) + 1)
    # unique_counters.sort()  # Sort the unique counter values
    #
    # # Create a histogram with integer counter values
    # plt.hist(counter_values, bins=unique_counters, align='left', rwidth=0.8)
    # plt.xlabel('Counter')
    # plt.ylabel('Frequency')
    # plt.xticks(unique_counters)  # Set x-axis ticks to unique counters
    # plt.title('Counter Frequency')
    # plt.show()


if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort='cumulative')
