"""Standard directories
"""
import skippy.config

import os


def initdirs():
    """Init standard dirs
    """
    makedir(skippy.config.LOGS_FOLDER)
    makedir(skippy.config.PROPERTY_FOLDER)


def makedir(path: str):
    """Make a directory if it doesn't exist
    
    Args:
        path (str): Path to folder
    """
    if not os.path.isdir(path):
        os.makedirs(path)
