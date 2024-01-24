import math
from FieldClass import *


def add_poly(p1, p2, p):
    return [(c1 + c2) % p for c1, c2 in zip(p1, p2)]


def sub_poly(p1, p2, p):
    return [(c1 - c2) % p for c1, c2 in zip(p1, p2)]


def mul_poly(p1, p2, p):
    result = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] = (result[i + j] + p1[i] * p2[j]) % p
    return result


def inv_mod_p(a, p):
    return pow(a, -1, p)


def div_poly(A, B):
    Q = Poly([0], A.field)
    R = Poly(A.coefficients.copy(), A.field)

    while len(R.coefficients) >= len(B.coefficients) and any(c != 0 for c in R.coefficients):
        a_i, b_j = R.coefficients[0], B.coefficients[0]
        term = [a_i * inv_mod_p(b_j, A.field.p) % A.field.p] + [0] * (len(R.coefficients) - len(B.coefficients))
        Q = Q.add(Poly(term, A.field), False)
        R = R.subtract(Poly(mul_poly(term, B.coefficients, A.field.p), A.field), False)

    return Q, R


def array_of_2(arr):
    if isinstance(arr, Poly):
        arr = arr.coefficients

    # Find the index of the first non-zero element
    non_zero_index = -1
    for i, x in enumerate(arr):
        if x != 0:
            non_zero_index = i
            break

    # non_zero_index = next((i for i, x in enumerate(arr) if x != 0), None)

    if non_zero_index != -1:
        # Slice the array from the first non-zero element onward
        result = arr[non_zero_index:]
        if len(result) == 1:
            return [0] + result
        return result
    else:
        # If the array is all zeros, return a single-element array with 0
        return [0, 0]


# Function to find modulo inverse of b. It returns
# -1 when inverse doesn't
# modInverse works for prime m
def mod_inverse(b, m):
    g = math.gcd(b, m)
    if g != 1:
        # print("Inverse doesn't exist")
        return -1
    else:
        # If b and m are relatively prime,
        # then modulo inverse is b^(m-2) mode m
        return pow(b, m - 2, m)


# Function to compute a/b under modulo m
def mod_divide(a, b, m):
    a = a % m
    inv = mod_inverse(b, m)
    if inv == -1:
        print("Division not defined")
    else:
        return (inv*a) % m


def is_int(a):
    # Find the index of the first non-zero element
    non_zero_index = next((i for i, x in enumerate(a.coefficients) if x != 0), None)

    if non_zero_index is not None:
        # Slice the array from the first non-zero element onward
        result = a.coefficients[non_zero_index:]
        if len(result) == 1:
            return True
        return False
    else:
        # If the array is all zeros
        return True


class Poly:
    def __init__(self, coefficients, field):
        self.coefficients = array_of_2(coefficients)
        self.field = field

    def add(self, other, flag):
        len_self, len_other = len(self.coefficients), len(other.coefficients)
        if len_self < len_other:
            self.coefficients = [0] * (len_other - len_self) + self.coefficients
        elif len_other < len_self:
            other.coefficients = [0] * (len_self - len_other) + other.coefficients
        if flag:
            result = [sum(pair) for pair in zip(self.coefficients, other.coefficients)]
        else:
            result = [sum(pair) % self.field.p for pair in zip(self.coefficients, other.coefficients)]
        return Poly(result, self.field)

    def subtract(self, other, flag):
        len_self, len_other = len(self.coefficients), len(other.coefficients)
        if len_self < len_other:
            self.coefficients = [0] * (len_other - len_self) + self.coefficients
        elif len_other < len_self:
            other.coefficients = [0] * (len_self - len_other) + other.coefficients
        if flag:
            result = [diff for diff in (a - b for a, b in zip(self.coefficients, other.coefficients))]
        else:
            result = [diff % self.field.p for diff in (a - b for a, b in zip(self.coefficients, other.coefficients))]
        return Poly(result, self.field)

    def multiply(self, other):
        result = mul_poly(self.coefficients, other.coefficients, self.field.p)
        res = Poly(result, self.field)
        return res.divide(Poly(self.field.irreduciblePolynomial, self.field))[1]

    def divide(self, other):
        # q, r = div_poly(self, other, self.field.p)
        q, r = div_poly(self, other)
        quotient = Poly(q, self.field)
        remainder = Poly(r, self.field)
        return quotient, remainder

    def pow(self, number):
        if number < self.field.p:  # x^(EFq)
            return self.pow2(number)
        array = [self.coefficients[0]] + [0] * (self.field.p - 1) + [self.coefficients[1]]
        if number % self.field.p == 0 and number != self.field.p:  # x^(EFq*p)
            return (Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]).pow(int(number/self.field.p))
        if number == self.field.p:  # x^(p)
            return Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]
        else:  # x^(EFq+p)
            return (Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]).multiply(self.pow(number-self.field.p))

    def pow2(self, number):
        if number == 0:
            return Poly([0, 1], self.field)  # x^0 = 1
        elif number == 1:
            return self

        # Use dynamic programming to avoid redundant calculations
        powers = {1: Poly(self.coefficients.copy(), self.field)}
        result = Poly([0, 1], self.field)
        current_power = 1
        current_squared = powers[1]

        while current_power * 2 <= number:
            current_power *= 2
            current_squared = current_squared.multiply(current_squared)
            powers[current_power] = current_squared

        remaining_power = number - current_power
        remaining_result = self.pow2(remaining_power)

        return result.multiply(current_squared.multiply(remaining_result))

    def __str__(self):
        terms = []
        reversed_coefficients = self.coefficients[::-1]
        for i, coef in enumerate(reversed_coefficients):
            if coef != 0:
                if i == 0:
                    terms.append(str(coef))
                elif i == 1 and coef == 1:
                    terms.append(f"x")
                elif i == 1:
                    terms.append(f"{coef}x")
                elif coef == 1:
                    terms.append(f"x^{i}")
                else:
                    terms.append(f"{coef}x^{i}")
        if not terms:
            return "0"
        else:
            return " + ".join(terms[::-1])

# Example usage:
# p_value = 7
# finite_field = field(p_value, None)
#
# A_coefficients = [6,3,1,1,0,1]
# B_coefficients = [3,5,6]
#
#
# A_poly = Poly(A_coefficients, finite_field)
# B_poly = Poly(B_coefficients, finite_field)
#
# # Perform polynomial division
# Q_poly, R_poly = A_poly.divide(B_poly)

# p_value = 2
# finite_field = field(p_value, None)
# C_coefficients = [1, 1]
# C_poly = Poly(C_coefficients, finite_field)
#
# res_poly = C_poly.pow2(3)
#
# print(C_poly.field.irreduciblePolynomial)
# print("res_poly:", res_poly)

# print("A(x):", A_poly)
# print("B(x):", B_poly)
# print("Quotient Q(x):", Q_poly)
# print("Remainder R(x):", R_poly)
# print("A(x)^p:", A_poly.pow(7))
# print("A(x)^p:", str(A_poly.pow(7)))
#
# print(array_of_2([0,0]))
