from __future__ import print_function
from timeit import Timer


def bench(stmt='pass', setup='pass'):
    """ BenchMark the function.

    """
    timer = Timer(stmt, setup)
    for i in range(100):
        number = 10**i
        time = timer.timeit(number)
        if time > 0.2:
            break

    times = [timer.timeit(number) for i in range(5)]
    message = '{} calls, best of 5 repeats: {:f} sec per call'
    return message.format(number, min(times)/number)
