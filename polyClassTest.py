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
            result[i + j] = (result[i + j] + p1[i] * p2[j])
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
        arr = arr.coefficients
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
            self.coefficients = [0] * (len_other - len_self) + self.coefficients
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
        return (Poly(result, self.field)).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]

    def divide(self, other):
        q, r = div_poly(self, other, self.field.p)
        quotient = Poly(q, self.field)
        remainder = Poly(r, self.field)
        return quotient, remainder

    def pow(self, number):
        if number < self.field.p:  # x^(EFq)
            res_mul = Poly(self.coefficients.copy(), self.field)
            for i in range(number-1):
                res_mul = res_mul.multiply(self)
            return res_mul
        try:
            array = [self.coefficients[0]] + [0] * (self.field.p - 1) + [self.coefficients[1]]
        except:
            self.coefficients = [0] + self.coefficients
            array = [self.coefficients[0]] + [0] * (self.field.p - 1) + [self.coefficients[1]]
        if number % self.field.p == 0 and number != self.field.p:  # x^(EFq*p)
            return (Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]).pow(int(number/self.field.p))
        if number == self.field.p:  # x^(p)
            return Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]
        else:  # x^(EFq+p)
            return (Poly(array, self.field).divide(Poly(self.field.irreduciblePolynomial, self.field))[1]).multiply(self.pow(number-self.field.p))

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
                    terms.append(f"{coef}*x")
                elif coef == 1:
                    terms.append(f"x^{i}")
                else:
                    terms.append(f"{coef}*x^{i}")
        if not terms:
            return "0"
        else:
            return " + ".join(terms[::-1])

# Example usage:
# p_value = 7
# finite_field = field(p_value)
#
# A_coefficients = [6,3,1,1,0,1]
# B_coefficients = [3,5,6]
#
# A_poly = Poly(A_coefficients, finite_field)
# B_poly = Poly(B_coefficients, finite_field)
#
# # Perform polynomial division
# Q_poly, R_poly = A_poly.divide(B_poly)
#
# print("A(x):", A_poly)
# print("B(x):", B_poly)
# print("Quotient Q(x):", Q_poly)
# print("Remainder R(x):", R_poly)
# print("A(x)^p:", A_poly.pow(7))
# print("A(x)^p:", str(A_poly.pow(7)))

