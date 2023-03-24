import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)


# index 0 is the coefficient of the 0th power of x, index 1 is the coeffiecient of the 1st power of x...

small = 0.0000000001  # minimum distance between zeroes, also dont change this because this is empirically the smallest value that works
compare = 10 ** -12  # evaluation of a zero will be at least this close to zero


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
            abs(evaluate_poly(poly, best_guess)) >= compare)
        # if the slope is too steep python cant find an x-coord that evaluates really close to zero
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


# zeroes should probably be  called list_CP because its a list of zeroes of derivatives
def zero_cp(poly: list) -> list:
    new_zeroes = []
    if len(poly) == 2:  # poly is a line
        return [line_zero(poly)]

    elif len(poly) == 3:  # poly is a quadratic and im not doing quadractic formula because it is lame
        zeroes = zero_cp(derivative(poly))
        CP = zeroes[0]
        if abs(evaluate_poly(poly, CP)) <= small:  # if vertex is the zero
            new_zeroes += [CP]
            return new_zeroes
        best_guess = -small + CP

        # there are no zeroes
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
    highest_zero = True
    index = len(poly) - 1

    while highest_zero:
        if poly[index] == 0:
            del poly[index]
        else:
            highest_zero = False
        index -= 1

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


