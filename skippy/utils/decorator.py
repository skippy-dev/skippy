###############################################################################
# Decorator decorator is a simplified version of the code from the funcy lib.
# https://github.com/Suor/funcy
###############################################################################

import functools
import inspect


class Call:
    def __init__(self, func, args, kwargs):
        self.func, self.args, self.kwargs = func, args, kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


def decorator(deco):
    spec = inspect.getargspec(deco)
    if len(spec.args) > 1 or spec.varargs or spec.keywords:

        @functools.wraps(deco)
        def _fab(*dargs, **dkwargs):
            return make_decorator(deco, *dargs, **dkwargs)

        return _fab
    else:
        return functools.wraps(deco)(make_decorator(deco))


def make_decorator(deco, *dargs, **dkwargs):
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            call = Call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)

        return wrapper

    return _decorator
