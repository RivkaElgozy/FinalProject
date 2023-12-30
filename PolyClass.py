from polynomial import Polynomial


class poly:
    def __init__(self, coeffs):
        self.pol = Polynomial(coeffs)
        self.coeffs = coeffs

    def add_polynomials(self, p, poly1, poly2):
        return self.get_poly_modP(p, poly1.pol + poly2.pol)

    def sub_polynomials(self, p, poly1, poly2):
        return self.get_poly_modP(p, poly1.pol - poly2.pol)

    def multiply_polynomials(self, p, poly1, poly2, coeffs_irreducible_poly):
        return self.get_poly_modP(p, divmod(poly1.pol * poly2.pol, Polynomial(coeffs_irreducible_poly))[1])

    def divide_polynomials(self, p, poly1, poly2, coeffs_irreducible_poly):
        return self.get_poly_modP(p, divmod(poly1.pol / poly2.pol, Polynomial(coeffs_irreducible_poly))[1])

    def pow(self, number):
        return poly([self.pol.a] + [0] * (number - 1) + [self.pol.b])

    def get_poly_modP(self, p, polynomial):
        return poly([elem % p for elem in polynomial[:]][::-1])



