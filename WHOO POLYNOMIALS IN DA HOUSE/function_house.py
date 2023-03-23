import poly_precision as prec
import polynomial_solving_funcs as ps


def clean_solve(poly):
    return prec.precision(poly, ps.poly_roots(poly), 0.1)


poly = [0, 0, 0, -20.5, 4, 0, 0, 6, -1]
print(prec.precision(poly, ps.poly_roots(poly), 0.1))
