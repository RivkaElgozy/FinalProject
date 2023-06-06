from polynomial import Polynomial
import sympy
import numpy as np


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
                poly = sympy.Poly(a * x**2 + b * x + c,x)
                if not any(poly.subs(x, i) % p == 0 for i in range(p)):
                    return poly
    return None


def find_polynomials(p, coeffs_irreducible_poly):
    x = sympy.Symbol('x')
    result = []
    for a in range(p):
        for b in range(p):
            w = Polynomial(a, b)
            #print("w: " + str(w))
            remainder = w
            for i in range(p - 1):
                remainder = divmod(w * remainder, Polynomial(coeffs_irreducible_poly))[1]
            remainder = remainder + w
            #print("remainder: " + str(remainder))
            remainder_mod_p = [elem % p for elem in remainder[:]][::-1]
            #print("remainder_mod_p: " + str(Polynomial(remainder_mod_p)))
            for c in range(p):
                for d in range(p):
                    t = Polynomial(c, d)
                    #print("t: " + str(t))
                    remainder2 = t
                    for i in range(p):
                        remainder2 = divmod(t * remainder2, Polynomial(coeffs_irreducible_poly))[1]
                    #print("remainder2: " + str(remainder2))
                    remainder2_mod_p = [elem % p for elem in remainder2[:]][::-1]
                    #print("remainder2_mod_p: " + str(Polynomial(remainder2_mod_p)))
                    if Polynomial(remainder_mod_p) == Polynomial(remainder2_mod_p):
                        result.append((w, t))
    print("Number of (w,t): " + str(len(result)))
    return result

def find_polynomials2(p, coeffs_irreducible_poly):
    x = sympy.Symbol('x')
    result = []
    for a in range(p):
        for b in range(p):
            # calculate w^p+w:
            w = Polynomial(a, b)
            arrW = [a] + [0] * (p-1) + [b]
            wPowP = Polynomial(arrW)
            remainderW = divmod(wPowP, Polynomial(coeffs_irreducible_poly))[1]
            remainderW = remainderW + w
            remainderW_mod_p = [elem % p for elem in remainderW[:]][::-1]
            for c in range(p):
                for d in range(p):
                    # calculate t^(p+1)
                    t = Polynomial(c, d)
                    arrT = [c] + [0] * (p-1) + [d]
                    tPowP = Polynomial(arrT)
                    remainderT = divmod(tPowP, Polynomial(coeffs_irreducible_poly))[1]
                    remainderT = divmod(t * remainderT, Polynomial(coeffs_irreducible_poly))[1]
                    remainderT_mod_p = [elem % p for elem in remainderT[:]][::-1]
                    if Polynomial(remainderW_mod_p) == Polynomial(remainderT_mod_p):
                        result.append((w, t))
    print("Number of (w,t): " + str(len(result)))
    return result


def main():
    p = get_prime()
    irreducible_poly = find_irreducible_poly(p)
    print(f"Irreducible polynomial: {irreducible_poly.as_expr()}")
    coeffs_irreducible_poly = irreducible_poly.all_coeffs()
    #polynomials = find_polynomials(p, coeffs_irreducible_poly)
    polynomials2 = find_polynomials2(p, coeffs_irreducible_poly)
    #print("Found polynomials w, t that satisfy the equation:")
    #for w, t in polynomials:
        #print(f"w = {w}, t = {t}")

    print("Found polynomials w, t that satisfy the equation:")
    for w, t in polynomials2:
        print(f"w = {w}, t = {t}")


if __name__ == "__main__":
    main()
