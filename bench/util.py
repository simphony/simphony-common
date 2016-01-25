from __future__ import print_function
from timeit import Timer


def bench(stmt='pass', setup='pass', repeat=5, adjust_runs=True):
    """ BenchMark the function.

    """
    timer = Timer(stmt, setup)
    if adjust_runs:
        for i in range(100):
            number = 10**i
            time = timer.timeit(number)
            if time > 0.2:
                break
    else:
        number = 1
    times = [timer.timeit(number) for i in range(repeat)]
    message = '{} calls, best of {} repeats: {:f} sec per call'
    return message.format(number, repeat, min(times)/number)
