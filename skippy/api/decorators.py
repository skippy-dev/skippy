###############################################################################
# Decorator decorator is a simplified version of the code from the funcy lib.
# https://github.com/Suor/funcy
###############################################################################
from skippy.gui import CriticalMessageBox

from skippy.utils.logger import log

import functools
import traceback
import inspect


class Call:
    """A call object to pass as first argument to decorator.

    Call object is just a proxy for decorated function
    with call arguments saved in its attributes.
    """

    def __init__(self, func, args, kwargs):
        self.func, self.args, self.kwargs = func, args, kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


def decorator(deco):
    """Transforms a flat wrapper into decorator."""
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


@decorator
def critical(call):
    """Log error and show critical message."""
    try:
        return call()
    except Exception as error:
        log.error(error, exc_info=True)
        CriticalMessageBox(type(error).__name__, traceback.format_exc()).exec_()


@decorator
def ignore(call, error=Exception, value=None):
    """Ignore selected error and return value (if selected)."""
    try:
        return call()
    except error:
        return value


@decorator
def debug(call):
    log.debug(
        f"""Function {call.func.__name__}('{"', '".join(map(str, call.args))}{"', '".join([f'{str(kwarg)}={str(call.kwargs[kwarg])}' for kwarg in call.kwargs])}')"""
    )
    result = call()
    log.debug(f"Function {call.func.__name__}(...) --> {result}")

    return result


__all__ = ["critical", "ignore", "debug"]
