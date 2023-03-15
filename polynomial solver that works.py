import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)


# index 0 is the coefficient of the 0th power of x, index 1 is the coeffiecient of the 1st power of x...

small = 0.000000001


def derivative(poly: list) -> list:
    derivative = []
    # no 0 because constants are taken out of derivative
    for power in range(1, len(poly)):
        derivative += [power * poly[power]]
    return derivative


def line_zero(b_m: list) -> float:
    return -b_m[0] / b_m[1]


def evaluate_poly(poly: list, x_coord: int) -> list:
    y_coord = 0
    for power in range(len(poly)):
        y_coord += poly[power] * x_coord ** power
    return y_coord


def tangent_zero(poly, x_coord):
    m = (evaluate_poly(derivative(poly), x_coord))
    b_m = [(evaluate_poly(poly, x_coord) - m * x_coord), m]
    return line_zero(b_m)


def nth_derivative(poly: list, n) -> list:
    for i in range(n):
        poly = derivative(poly)
    return poly


def zero_cp(poly: list) -> list:  # zeroes should probably be  called list_CP
    new_zeroes = []
    if len(poly) == 2:
        return [line_zero(poly)]

    elif len(poly) == 3:
        zeroes = zero_cp(derivative(poly))
        CP = zeroes[0]
        best_guess = -small + CP
        not_zero = True

        if evaluate_poly(poly, CP) * evaluate_poly(derivative(poly), CP + small) > 0:
            return new_zeroes

        while not_zero:  # left-most zero
            best_guess = tangent_zero(poly, best_guess)
            not_zero = (
                abs(evaluate_poly(poly, best_guess)) >= small)

        new_zeroes += [best_guess]
        best_guess = small + CP
        not_zero = True

        while not_zero:  # left-most zero
            best_guess = tangent_zero(poly, best_guess)
            not_zero = (
                abs(evaluate_poly(poly, best_guess)) >= small)

        new_zeroes += [best_guess]
        return new_zeroes

    else:

        zeroes = zero_cp(derivative(poly))
        POI = zero_cp(nth_derivative(poly, 2))
        if zeroes is None:
            zeroes = []
        if zeroes == []:
            best_guess = 1.5
            not_zero = True
            while not_zero:  # left-most zero
                best_guess = tangent_zero(poly, best_guess)
                not_zero = (
                    abs(evaluate_poly(poly, best_guess)) >= small)

            new_zeroes += [best_guess]

            return new_zeroes

        elif len(zeroes) == 1:
            not_zero = True
            CP = zeroes[0]
            best_guess = -small + CP

            if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) > 0:

                while not_zero:  # left-most zero
                    best_guess = tangent_zero(poly, best_guess)
                    not_zero = (
                        abs(evaluate_poly(poly, best_guess)) >= small)

                new_zeroes += [best_guess]

            best_guess = small + CP

            if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) < 0:
                while not_zero:  # left-most zero
                    best_guess = tangent_zero(poly, best_guess)
                    not_zero = (
                        abs(evaluate_poly(poly, best_guess)) >= small)

                new_zeroes += [best_guess]

        else:

            for index in range(len(zeroes)):
                CP = zeroes[index]

                if index != len(zeroes) - 1:
                    CP_right = zeroes[index + 1]

                not_zero = True
                if abs(evaluate_poly(poly, CP)) <= small:
                    new_zeroes += [CP]

                else:
                    if index == 0:  # left-most CP
                        best_guess = -small + CP
                        if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) > 0:

                            while not_zero:  # left-most zero
                                best_guess = tangent_zero(poly, best_guess)
                                not_zero = (
                                    abs(evaluate_poly(poly, best_guess)) >= small)

                            new_zeroes += [best_guess]

                        best_guess = small + CP
                        not_zero = True

                        # one of the in-betweens (i died)
                        if (evaluate_poly(poly, CP_right) - evaluate_poly(poly, CP)) * evaluate_poly(derivative(poly), best_guess) > 0:

                            best_guess = tangent_zero(
                                nth_derivative(poly, 2), POI[index])
                            while not_zero:  # left-most zero
                                best_guess = tangent_zero(poly, best_guess)
                                not_zero = (
                                    abs(evaluate_poly(poly, best_guess)) >= small)

                            new_zeroes += [best_guess]

                    elif index == len(zeroes) - 1:  # right-most zero
                        best_guess = small + CP
                        if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) < 0:
                            while not_zero:  # left-most zero
                                best_guess = tangent_zero(poly, best_guess)
                                not_zero = (
                                    abs(evaluate_poly(poly, best_guess)) >= small)

                            new_zeroes += [best_guess]

                    else:  # one of the in-betweens
                        best_guess = small + CP

                        if (evaluate_poly(poly, CP_right) - evaluate_poly(poly, CP)) * evaluate_poly(derivative(poly), best_guess) > 0:

                            best_guess = tangent_zero(
                                nth_derivative(poly, 2), POI[index])
                            while not_zero:  # left-most zero
                                best_guess = tangent_zero(poly, best_guess)
                                not_zero = (
                                    abs(evaluate_poly(poly, best_guess)) >= small)

                            new_zeroes += [best_guess]
            return new_zeroes


def poly_roots(poly):
    zeroes = zero_cp(poly)
    rounded_zeroes = []
    if zeroes is None:
        return []
    for zero in zeroes:
        zero = round(zero, 4)
        if zero == -0:
            zero = 0
        rounded_zeroes += [zero]
    rounded_zeroes = list(dict.fromkeys(rounded_zeroes))

    return rounded_zeroes


degree = int(input("Enter degree of polynomial:"))
poly = []


for power in range(degree, -1, -1):
    print('Enter coefficient of x^', end='')
    print(str(power), end=' : ')
    poly += [(float(input()))]

poly.reverse()
print(poly_roots(poly))


