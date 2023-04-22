import sympy
from sympy import *

x = sympy.Symbol('x')

p = 5 # your chosen prime number
F = GF(p)
a = 3
b = 4
f = a*x + b
print(f)
g = x + 1
h = f + g
print(h)

w = f*h
print(sympy.expand(w))

#u = sympy.random_poly(x, 1, 0, 7)
#print(f'u + {u}')
# print(real_root(u))
#w = sympy.rem(f*h,x**2+x+1)
#print(sympy.expand(w))
d = sympy.red(x,GF,p)
print(d)
