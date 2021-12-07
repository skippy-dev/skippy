"""Standard directories
"""
from skippy.utils import is_frozen

import skippy.config

import os


def initdirs():
    """Init standard dirs"""
    if is_frozen():
        makedir(skippy.config.APPDATA_FOLDER)
    makedir(skippy.config.LOGS_FOLDER)
    makedir(skippy.config.PROPERTY_FOLDER)
    makedir(skippy.config.PLUGINS_SETTINGS_FOLDER)


def makedir(path: str):
    """Make a directory if it doesn't exist

    Args:
        path (str): Path to folder
    """
    if not os.path.isdir(path):
        os.makedirs(path)
