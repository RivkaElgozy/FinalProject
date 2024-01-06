import sympy
from FieldClass import field
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

def div_poly(A, B, p):
    Q = Poly([0], A.field)  # Initialize Q as Poly([0], A.field)
    R = Poly(A.coefficients.copy(),A.field)

    while len(R.coefficients) >= len(B.coefficients) and any(c != 0 for c in R.coefficients):
        a_i, b_j = R.coefficients[0], B.coefficients[0]
        term = [a_i * inv_mod_p(b_j, p) % p] + [0] * (len(R.coefficients) - len(B.coefficients))
        Q = Q.add(Poly(term, A.field))
        R = R.subtract(Poly(mul_poly(term, B.coefficients, p), A.field))
    return Q, R

def remove_leading_zeros(arr):
    if isinstance(arr,Poly):
        arr=arr.coefficients
    # Find the index of the first non-zero element
    non_zero_index = next((i for i, x in enumerate(arr) if x != 0), None)

    if non_zero_index is not None:
        # Slice the array from the first non-zero element onward
        result = arr[non_zero_index:]
        return result
    else:
        # If the array is all zeros, return a single-element array with 0
        return [0]


class Poly:
    def __init__(self, coefficients, field):
        self.coefficients = remove_leading_zeros(coefficients)
        self.field = field

    def add(self, other):
        len_self, len_other = len(self.coefficients), len(other.coefficients)

        if len_self < len_other:
            self.coefficients += [0] * (len_other - len_self)
        elif len_other < len_self:
            other.coefficients = [0] * (len_self - len_other) + other.coefficients

        result = [sum(pair) % self.field.p for pair in zip(self.coefficients, other.coefficients)]
        return Poly(result, self.field)

    def subtract(self, other):
        len_self, len_other = len(self.coefficients), len(other.coefficients)

        if len_self < len_other:
            self.coefficients += [0] * (len_other - len_self)
        elif len_other < len_self:
            other.coefficients = [0] * (len_self - len_other) + other.coefficients

        result = [diff % self.field.p for diff in (a - b for a, b in zip(self.coefficients, other.coefficients))]
        return Poly(result, self.field)
    def multiply(self, other):
        result = mul_poly(self.coefficients, other.coefficients, self.field.p)
        return Poly(result, self.field)

    def divide(self, other):
        q, r = div_poly(self, other, self.field.p)
        quotient = Poly(q, self.field)
        remainder = Poly(r, self.field)
        return quotient, remainder

    def __str__(self):
        return f"Poly({self.coefficients}, {self.field.p})"

# Example usage:
p_value = 7
finite_field = field(p_value)

A_coefficients = [6,3,1,1,0,1]
B_coefficients = [3,5,6]

A_poly = Poly(A_coefficients, finite_field)
B_poly = Poly(B_coefficients, finite_field)

# Perform polynomial division
Q_poly, R_poly = A_poly.divide(B_poly)

print("A(x):", A_poly)
print("B(x):", B_poly)
print("Quotient Q(x):", Q_poly)
print("Remainder R(x):", R_poly)