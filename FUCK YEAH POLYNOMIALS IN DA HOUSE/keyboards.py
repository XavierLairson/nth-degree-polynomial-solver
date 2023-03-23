import poly_solver
import poly_precision

degree = int(input("Enter degree of polynomial:"))
poly = []


for power in range(degree, -1, -1):
    print('Enter coefficient of x^', end='')
    print(str(power), end=' : ')
    poly += [(float(input()))]

poly.reverse()
print(poly_solver.poly_roots(poly))
