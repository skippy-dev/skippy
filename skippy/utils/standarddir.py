"""Standard directories
"""
from skippy.utils import is_frozen

import skippy.config

from pathlib import Path


def initdirs():
    """Init standard dirs"""
    if is_frozen():
        makedir(skippy.config.APPDATA_FOLDER)
    makedir(skippy.config.LOGS_FOLDER)
    makedir(skippy.config.PROPERTY_FOLDER)
    makedir(skippy.config.PLUGINS_SETTINGS_FOLDER)


def makedir(path: Path):
    """Make a directory if it doesn't exist

    Args:
        path (Path): Path to folder
    """
    if not path.is_dir():
        path.mkdir()
