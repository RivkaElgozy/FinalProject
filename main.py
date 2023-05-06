import math
from sympy import *
import numpy as np
import random
import sympy
import galois

def find_poly(p):
    for a in range(p):
        for b in range(p):
            for c in range(p):
                poly = sympy.Poly([a, b, c], x, domain=F)
                if not poly.is_irreducible:
                    poly_str = str(poly.as_expr())
                    print(f"The polynomial {poly_str} has no roots.")
                    return poly

def polynomial_add_Fq(A, B, q):
    result = [0] * max(len(A), len(B))
    for i in range(len(result)):
        a = A[i] if i < len(A) else 0
        b = B[i] if i < len(B) else 0
        result[i] = (a + b) % q
    return result

def polynomial_power_GF(p, n, poly, polyX):
    GF = galois.GF(p**n)
    polyX_GF = galois.Poly(polyX, field=GF)
    poly_GF = galois.Poly(poly, field=GF)

    result_GF = (polyX_GF ** p) % poly_GF
    return result_GF.coeffs.tolist()

x = sympy.Symbol('x')
np.random.seed(123)

user_input = input("Enter your prime number: ")
p = int(user_input)
degree = 2
F = GF(p ** degree)
polynomials = []

# Loop until we find a polynomial with no roots
# while True:
#     # Generate a random polynomial
#     #poly = random_poly(x, 0, p-1, domain=F, polys=true)
#     a = np.random.randint(0, p)
#     b = np.random.randint(0, p)
#     poly = sympy.Poly([a, b], x, domain=F)
#     print(poly)
#
#     # Check if the polynomial has any roots
#     if not poly.is_irreducible:
#         # The polynomial has no roots, so print it and exit the loop
#         #print(f"The polynomial {str(poly)} has no roots.")
#         poly_str = str(poly.as_expr())
#         print(f"The polynomial {poly_str} has no roots.")
#         break

poly = find_poly(p)


for a in range(p):
    for b in range(p):
        poly1 = sympy.Poly(a*x + b, x)
        polynomials.append(poly1)

for polyX in polynomials:
    print("polyX: " + str(polyX.as_expr()))
    coeffsX = polyX.all_coeffs()
    coeffsp = poly.all_coeffs()
    #reminderX = sum(c * x ** (p * i) for i, c in enumerate(coeffsX)) % poly
    #pX_coeffs = [(c ** p % p) for c in coeffsX]
    #pX = sympy.Poly(pX_coeffs, x, domain=F) + reminderX
    #reminderX = (sympy.Poly(polyX ** p, domain=F).div(poly, F))[1]
    remindercoeffsX = polynomial_power_GF(p, degree, coeffsp, coeffsX)
    reminderX = sympy.Poly(remindercoeffsX, x, domain=F)
    print("reminderX: " + str(reminderX.as_expr()))
    coeffsReminderX = reminderX.all_coeffs()
    coeffsPolyX = polyX.all_coeffs()
    coeffsPX = polynomial_add_Fq(coeffsReminderX, coeffsPolyX, p)
    pX = sympy.Poly(coeffsPX, x, domain=F)
    print("pX: " + str(pX.as_expr()))
    for polyY in polynomials:
        #coeffsY = polyY.all_coeffs()
        #reminderY = sum(c * x ** (p * i) for i, c in enumerate(coeffsY)) % poly
        reminderY = (sympy.Poly(polyY ** (p+1), domain=F).div(poly, F))[1]
        # print("reminderY: " + str(reminderY.as_expr()))
        # if pX.as_expr() == reminderY.as_expr():
        #     print("There is a match: ")
        #     print(pX.as_expr())





# import sympy
#
# def get_prime():
#     while True:
#         p = int(input("Enter a prime number: "))
#         if sympy.isprime(p):
#             break
#         else:
#             print("The number is not prime. Please enter a prime number.")
#     return p
#
# def find_irreducible_poly(p):
#     x = sympy.Symbol('x')
#     for a in range(1, p):
#         for b in range(p):
#             for c in range(p):
#                 poly = a * x**2 + b * x + c
#                 if not any(poly.subs(x, i) % p == 0 for i in range(p)):
#                     return poly
#     return None
#
# def polynomial_division_Fq(A, B, q):
#     def polynomial_mod(poly, p):
#         return [coefficient % p for coefficient in poly]
#
#     def polynomial_degree(poly):
#         return len(poly) - 1
#
#     def polynomial_divide(poly1, poly2):
#         if polynomial_degree(poly1) < polynomial_degree(poly2):
#             return ([0], poly1)
#         else:
#             leading_term_division = poly1[-1] * pow(poly2[-1], -1, q) % q
#             new_poly1 = [i - j * leading_term_division for i, j in zip(poly1, poly2 + [0] * (polynomial_degree(poly1) - polynomial_degree(poly2)))]
#             quotient, remainder = polynomial_divide(new_poly1[:-1], poly2)
#             return (quotient + [leading_term_division], remainder)
#
#     A = polynomial_mod(A, q)
#     B = polynomial_mod(B, q)
#
#     if polynomial_degree(A) < polynomial_degree(B):
#         return A
#     else:
#         _, remainder = polynomial_divide(A, B)
#         return remainder
#
# def find_polynomials(p, irreducible_poly):
#     x = sympy.Symbol('x')
#     result = []
#     for a in range(p):
#         for b in range(p):
#             w = a * x + b
#             for c in range(p):
#                 for d in range(p):
#                     t = c * x + d
#                     equation = w**p + w -t**(p+1)
#                     if equation.simplify() == 0:
#                         result.append((w, t))
#     return result
#
# def main():
#     p = get_prime()
#     irreducible_poly = find_irreducible_poly(p)
#     print(f"Irreducible polynomial: {irreducible_poly}")
#
#     polynomials = find_polynomials(p, irreducible_poly)
#     print("Found polynomials w, t that satisfy the equation:")
#     for w, t in polynomials:
#         print(f"w = {w}, t = {t}")
#
# if __name__ == "__main__":
#     main()




