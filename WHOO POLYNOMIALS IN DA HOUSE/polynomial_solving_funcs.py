import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)


# index 0 is the coefficient of the 0th power of x, index 1 is the coeffiecient of the 1st power of x...

small = 0.0000000001
compare = 10 ** -12


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


def zero_search(poly, best_guess):
    not_zero = True
    counter = 0
    best_prev = 0
    while not_zero and counter < 100:

        best_prev = best_guess
        best_guess = tangent_zero(poly, best_guess)
        not_zero = (
            abs(evaluate_poly(poly, best_guess)) >= small)
        if abs(best_prev - best_guess) < small:
            counter += 1
    return best_guess


def sort_ascending(arr):
    for i in range(len(arr) - 1):
        while(arr[i + 1]) < arr[i] and i >= 0:
            (arr[i + 1], arr[i]) = (arr[i], arr[1 + i])
            i -= 1
    return arr


def clean_up(zeroes):
    return sort_ascending(zeroes)


def zero_cp(poly: list) -> list:  # zeroes should probably be  called list_CP
    new_zeroes = []
    if len(poly) == 2:
        return [line_zero(poly)]

    elif len(poly) == 3:
        zeroes = zero_cp(derivative(poly))
        CP = zeroes[0]
        if abs(evaluate_poly(poly, CP)) <= small:
            new_zeroes += [CP]
            return new_zeroes
        best_guess = -small + CP

        if evaluate_poly(poly, CP) * evaluate_poly(derivative(poly), CP + small) > 0:
            return new_zeroes
        new_zeroes += [zero_search(poly, best_guess)]
        best_guess = small + CP
        new_zeroes += [zero_search(poly, best_guess)]
        return clean_up(new_zeroes)

    else:

        zeroes = zero_cp(derivative(poly))
        POI = zero_cp(nth_derivative(poly, 2))
        illegal_indexes = []

        if zeroes is None:
            zeroes = []
        if zeroes == []:
            best_guess = 1.5
            new_zeroes += [zero_search(poly, best_guess)]
            return clean_up(new_zeroes)

        elif len(zeroes) == 1:
            CP = zeroes[0]
            best_guess = -small + CP

            if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) > 0:
                new_zeroes += [zero_search(poly, best_guess)]

            best_guess = small + CP
            if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) < 0:
                new_zeroes += [zero_search(poly, best_guess)]
            return new_zeroes

        else:

            for index in range(len(zeroes)):
                CP = zeroes[index]

                if index != len(zeroes) - 1:
                    CP_right = zeroes[index + 1]

                if abs(evaluate_poly(poly, CP)) <= small:
                    new_zeroes += [CP]
                    illegal_indexes += [index]

                else:
                    if index == 0:  # left-most CP
                        if evaluate_poly(derivative(poly), CP - 100) * evaluate_poly(poly, CP) > 0:
                            new_zeroes += [zero_search(poly, CP - 10)]

                        start = POI[index]
                        POI_count = 1
                        while start < CP and POI_count + index < len(POI):
                            start = POI[index + POI_count]
                            POI_count += 1
                        next_CP = True
                        if abs(evaluate_poly(poly, zeroes[index + 1])) < compare:
                            next_CP = False
                        if evaluate_poly(poly, CP) * evaluate_poly(poly, zeroes[index + 1]) < 0 and next_CP:
                            new_zeroes += [zero_search(poly, start)]

                    elif index == len(zeroes) - 1:  # right-most zero
                        best_guess = small + CP
                        if evaluate_poly(derivative(poly), best_guess) * evaluate_poly(poly, CP) < 0:
                            new_zeroes += [zero_search(poly, best_guess)]

                    else:  # one of the in-betweens
                        start = POI[index]
                        POI_count = 1
                        while start < CP and POI_count + index < len(POI):
                            start = POI[index + POI_count]
                            POI_count += 1
                        next_CP = True
                        if abs(evaluate_poly(poly, zeroes[index + 1])) < compare:
                            next_CP = False
                        if evaluate_poly(poly, CP) * evaluate_poly(poly, zeroes[index + 1]) < 0 and next_CP:
                            new_zeroes += [zero_search(poly, start)]

            return clean_up(new_zeroes)


def poly_roots(poly):
    zeroes = zero_cp(poly)
    rounded_zeroes = []
    if zeroes is None:
        return []
    for zero in zeroes:
        zero = round(zero, 12)
        if zero == -0:
            zero = 0
        rounded_zeroes += [zero]
    rounded_zeroes = list(dict.fromkeys(rounded_zeroes))

    return rounded_zeroes


def factorial(num):
    if num == 1 or num == 0:
        return 1
    else:
        return num * factorial(num - 1)


def expand_cos(n_degree):
    power_series = []
    for power in range(0, n_degree + 1):
        if power % 4 == 0:
            power_series += [1 / factorial(power)]
        elif power % 2 == 0:
            power_series += [-1 / factorial(power)]
        else:
            power_series += [0]
    return power_series


def expand_sin(n_degree):
    power_series = []
    for power in range(0, n_degree + 1):
        if (power + 1) % 4 == 0:
            power_series += [-1 / factorial(power)]
        elif (power + 1) % 2 == 0:
            power_series += [1 / factorial(power)]
        else:
            power_series += [0]
    return power_series


def pi_finder(n_degrees):
    potentials = poly_roots(expand_cos(n_degrees))
    temp = []
    for index in range(len(potentials)):
        temp += [[abs(potentials[index] - 1.5), index]]
    for i in range(len(temp) - 1):
        while(temp[i + 1][0]) < temp[i][0] and i >= 0:
            (temp[i + 1], temp[i]) = (temp[i], temp[1 + i])
            i -= 1
    pi = 2 * potentials[temp[0][1]] * (2 * potentials[temp[0][1]] // 3)
    return pi


