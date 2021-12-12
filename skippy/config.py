"""Configures various variables used by Skippy.

Attributes:
    LANG_FOLDER (Path): Language folder
    LOGS_FOLDER (Path): Logs folder
    PLUGINS_FOLDER (Path): Plugins folder
    PROPERTY_FOLDER (Path): Property folder
    RESOURCES_FOLDER (Path): Resources folder
    SKIPPY_FOLDER (Path): Skippy folder
    version (Path): Skippy version same as skippy.__version__
"""
from skippy import __version__

from skippy.utils import is_frozen

from pathlib import Path
import os

version = __version__

SKIPPY_FOLDER = Path(os.path.dirname(os.path.realpath(__file__)))

RESOURCES_FOLDER = SKIPPY_FOLDER / "resources"

PROPERTY_FOLDER = SKIPPY_FOLDER / "property"

LOGS_FOLDER = SKIPPY_FOLDER / "logs"

LANG_FOLDER = SKIPPY_FOLDER / "lang"

PLUGINS_FOLDER = SKIPPY_FOLDER / "plugins"

PLUGINS_SETTINGS_FOLDER = PLUGINS_FOLDER / "settings"

if is_frozen():
    APPDATA_FOLDER = Path(os.getenv("APPDATA")) / "Skippy"

    PROPERTY_FOLDER = APPDATA_FOLDER / "property"

    LOGS_FOLDER = APPDATA_FOLDER / "logs"

    PLUGINS_SETTINGS_FOLDER = APPDATA_FOLDER / "plugins"
