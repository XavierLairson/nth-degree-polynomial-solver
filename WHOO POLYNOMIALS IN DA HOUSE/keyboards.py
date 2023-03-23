import function_house

degree = int(input("Enter degree of polynomial:"))
poly = []

for power in range(degree, -1, -1):
    print('Enter coefficient of x^', end='')
    print(str(power), end=' : ')
    poly += [(float(input()))]

poly.reverse()
print(function_house.clean_solve(poly))
