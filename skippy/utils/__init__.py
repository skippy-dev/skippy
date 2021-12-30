import pathlib
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


def get_datadir() -> pathlib.Path:

    """Returns a parent directory path where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming

    Returns:
        pathlib.Path: Data dir path
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming" / "Skippy"
    elif sys.platform == "darwin":
        return home / "Library/Application Support" / "Skippy"
    elif sys.platform.startswith('linux'):
        return home / ".local/share" / "Skippy"


__all__ = ["cached_property", "is_frozen", "get_datadir"]
