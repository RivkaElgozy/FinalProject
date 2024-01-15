import sympy


class field:
    def __init__(self, p, irreducible_polynomial):
        self.p = p
        if irreducible_polynomial is None:
            self.irreduciblePolynomial = self.get_irreducible_polynomial()
        else:
            self.irreduciblePolynomial = irreducible_polynomial

    def get_irreducible_polynomial(self):
        x = sympy.Symbol('x')
        for a in range(1, self.p):
            for b in range(self.p):
                for c in range(self.p):
                    poly = sympy.Poly(a * x ** 2 + b * x + c, x)
                    if not any(poly.subs(x, i) % self.p == 0 for i in range(self.p)):
                        return poly.all_coeffs()
        return None