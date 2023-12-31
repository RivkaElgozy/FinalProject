from polynomial import Polynomial
from FieldClass import field


class poly:
    def __init__(self, coeffs):
        self.pol = Polynomial(coeffs)
        self.coeffs = coeffs

    def add_polynomial(self, p, poly1):
        print("add: ", self.pol + poly1.pol)
        return self.get_poly_modP(p, Polynomial(self.pol + poly1.pol))

    def sub_polynomial(self, p, poly1):
        return self.get_poly_modP(p, Polynomial(self.pol - poly1.pol))

    def multiply_polynomial(self, poly1, field_p):
        return self.get_poly_modP(field_p.p, divmod(self.pol * poly1.pol, Polynomial(field_p.irreduciblePolynomial))[1])

    def divide_polynomial(self, poly1, field_p):
        return self.get_poly_modP(field_p.p, divmod(self.pol / poly1.pol, Polynomial(field_p.irreduciblePolynomial))[1])

    def pow(self, number, field_p):
        array = []
        if number % field_p.p == 0:
            try:
                array = [self.pol.a] + [0] * (field_p.p - 1) + [self.pol.b]
            except:
                array = [0] + [self.pol.a] + [0] * (field_p.p - 1)
            # return self.get_poly_modP(field_p.p, divmod(Polynomial(array), Polynomial(field_p.irreduciblePolynomial))[1][:])
            return poly(divmod(Polynomial(array), Polynomial(field_p.irreduciblePolynomial))[1][:])
        else:
            try:
                array = [self.pol.a] + [0] * (field_p.p - 1) + [self.pol.b]
            except:
                array = [0] + [self.pol.a] + [0] * (field_p.p - 1)
            res = self.pol
            for i in range(number % field_p.p):
                res = divmod(res * divmod(Polynomial(array), Polynomial(field_p.irreduciblePolynomial))[1], Polynomial(field_p.irreduciblePolynomial))[1]
            return self.get_poly_modP(field_p.p, res)


    def get_poly_modP(self, p, poly1):
        # Ensure that the array has a minimum size of 2
        array = [0] * max(0, 2 - len(poly1[:])) + poly1[:]
        # Perform modulus operation
        return poly([elem % p for elem in array])


