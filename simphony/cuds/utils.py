from functools import wraps
import warnings


def deprecated(func):
    @wraps(func)
    def _deprecated(*args, **kwargs):
        warnings.warn("Deprecation warning: {}".format(func.__name__))
        return func(*args, **kwargs)

    return _deprecated
