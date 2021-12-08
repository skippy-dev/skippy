"""Configures various variables used by Skippy.

Attributes:
    LANG_FOLDER (str): Language folder
    LOGS_FOLDER (str): Logs folder
    PLUGINS_FOLDER (str): Plugins folder
    PROPERTY_FOLDER (str): Property folder
    RESOURCES_FOLDER (str): Resources folder
    SKIPPY_FOLDER (str): Skippy folder
    version (str): Skippy version same as skippy.__version__
"""
from skippy import __version__

from skippy.utils import is_frozen

import os

version = __version__

SKIPPY_FOLDER = os.path.dirname(os.path.realpath(__file__))

RESOURCES_FOLDER = os.path.join(SKIPPY_FOLDER, "resources")

PROPERTY_FOLDER = os.path.join(SKIPPY_FOLDER, "property")

LOGS_FOLDER = os.path.join(SKIPPY_FOLDER, "logs")

LANG_FOLDER = os.path.join(SKIPPY_FOLDER, "lang")

PLUGINS_FOLDER = os.path.join(SKIPPY_FOLDER, "plugins")

if is_frozen():
    APPDATA_FOLDER = os.path.join(os.getenv("APPDATA"), "Skippy")

    PROPERTY_FOLDER = os.path.join(APPDATA_FOLDER, "property")

    LOGS_FOLDER = os.path.join(APPDATA_FOLDER, "logs")

    PLUGINS_SETTINGS_FOLDER = os.path.join(APPDATA_FOLDER, "plugins")

PLUGINS_SETTINGS_FOLDER = os.path.join(PLUGINS_FOLDER, "settings")
