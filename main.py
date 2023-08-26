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


def printPolyPoints(polynomials1):
    print("Found polynomials w, t that satisfy the equation:")
    for w, t in polynomials1:
        print(f"w = {w}, t = {t}")


def printLinearLine(a, b, p, coeffs_irreducible_poly):
    result = []
    for z1 in range(p):
        for z2 in range(p):
            z = Polynomial(z1,z2)
            w = a[0]
            t = a[1]
            wTag = b[0]
            tTag = b[1]
            #w:
            resW = w - wTag
            remainderW_mod_p = Polynomial([elem % p for elem in resW[:]][::-1])
            remainderW = divmod(z * remainderW_mod_p, Polynomial(coeffs_irreducible_poly))[1]
            res1 = remainderW + wTag
            res1_mod_p = Polynomial([elem % p for elem in res1[:]][::-1])
            #t:
            resT = t - tTag
            remainderT_mod_p = Polynomial([elem % p for elem in resT[:]][::-1])
            remainderT = divmod(z * remainderT_mod_p, Polynomial(coeffs_irreducible_poly))[1]
            res2 = remainderT + tTag
            res2_mod_p = Polynomial([elem % p for elem in res2[:]][::-1])
            result.append((res1_mod_p, res2_mod_p))
            #line = f"({wTag} + {z} * ({w} - {wTag}),({tTag} + {z} * ({t} - {tTag}))"
            #print("The equation of the line is: F(z) =", (res1_mod_p, res2_mod_p))
            #print(f"Fz1 = {res1_mod_p}, Fz2 = {res2_mod_p}")
    return result

def findLines(polynomials1,p, coeffs_irreducible_poly):
    result = []
    for a in polynomials1:
        for b in polynomials1:
            result += printLinearLine(a,b,p,coeffs_irreducible_poly)
            #test for each a,b
    return result

def matchesCounter(polynomials1, polynomials2):
    count = 0
    for w, t in polynomials2:#F_(a,b)z
        for w2, t2 in polynomials1:
            if w == w2 and t == t2:
                count += 1
                break

    print("Number of matching pairs:", count)



def main():
    p = get_prime()
    irreducible_poly = find_irreducible_poly(p)
    print(f"Irreducible polynomial: {irreducible_poly.as_expr()}")
    coeffs_irreducible_poly = irreducible_poly.all_coeffs()
    polynomials1 = find_polynomials2(p, coeffs_irreducible_poly)
    printPolyPoints(polynomials1)
    ########################################################
    polynomials2 = findLines(polynomials1,p, coeffs_irreducible_poly)
    #print(polynomials2)
    matchesCounter(polynomials1,polynomials2)



if __name__ == "__main__":
    main()
