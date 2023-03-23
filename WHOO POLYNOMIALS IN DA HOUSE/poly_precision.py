import polynomial_solving_funcs as ps


def try_again(poly, estimate, interval):
    best = 0
    relative = estimate / (10 ** 10)
    if ps.evaluate_poly(poly, estimate) == 0:
        best = estimate
    else:
        test = estimate - interval
        right_end = estimate + interval
        sample_list = []

        counter = 0
        while test < right_end and counter < 25:
            test_val = ps.evaluate_poly(poly, test)
            sample_list += [[test_val, test]]
            test += interval / 10
            counter += 1

        for index in range(1, len(sample_list)):
            if sample_list[index][0] == 0:  # see if test is precisely zero
                best = sample_list[index][1]

            # see if sign changes between tests
            if sample_list[index][0] * sample_list[index - 1][0] < 0:
                if abs(sample_list[index][0] - sample_list[index - 1][0]) < abs(relative):
                    best = sample_list[index][1]

                else:
                    next_best = try_again(
                        poly, sample_list[index][1], interval / 2)
                    best = next_best
    return best


def precision(poly, estimates_list, interval):
    best_list = []
    for estimate in estimates_list:
        relative = estimate / (10 ** 10)
        if ps.evaluate_poly(poly, estimate) == 0:
            best_list += [estimate]
        else:
            test = estimate - interval
            right_end = estimate + interval
            sample_list = []

            while test < right_end:
                test_val = ps.evaluate_poly(poly, test)
                sample_list += [[test_val, test]]
                test += interval / 100
            for index in range(1, len(sample_list)):
                if sample_list[index][0] == 0:  # see if test is precisely zero
                    best_list += [sample_list[index][1]]

                # see if sign changes between tests
                if sample_list[index][0] * sample_list[index - 1][0] < 0:
                    if abs(sample_list[index][0] - sample_list[index - 1][0]) < abs(relative):
                        best_list += [sample_list[index][1]]

                    else:
                        next_best = try_again(
                            poly, sample_list[index][1], interval / 2)
                        best_list += [next_best]
    return best_list










