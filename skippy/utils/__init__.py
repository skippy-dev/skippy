import sys

try:
    from functools import cached_property
except ImportError:
    from functools import lru_cache
    cached_property = lambda func: property(lru_cache(func))


def is_frozen() -> bool:
    """Is Skippy compiled to exe

    Returns:
        bool: Compiled or not
    """
    return getattr(sys, "frozen", False)


__all__ = ["cached_property", "is_frozen"]
