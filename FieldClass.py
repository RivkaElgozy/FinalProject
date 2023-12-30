import sympy

class field:
    def __init__(self, p):
        self.p = p
        self.irreduciblePolynomial = self.get_irreducible_polynomial()

    def get_irreducible_polynomial(self):
        x = sympy.Symbol('x')
        for a in range(1, self.p):
            for b in range(self.p):
                for c in range(self.p):
                    poly = sympy.Poly(a * x ** 2 + b * x + c, x)
                    if not any(poly.subs(x, i) % self.p == 0 for i in range(self.p)):
                        print(f"Irreducible polynomial: {poly.as_expr()}")
                        return poly.all_coeffs()
        return None