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

from skippy.utils import is_frozen, get_datadir

from pathlib import Path
import datetime
import os

version = __version__

SKIPPY_FOLDER = Path(os.path.dirname(os.path.realpath(__file__)))

RESOURCES_FOLDER = SKIPPY_FOLDER / "resources"

PROPERTY_FOLDER = SKIPPY_FOLDER / "property"

LOGS_FOLDER = SKIPPY_FOLDER / "logs"

LANG_FOLDER = SKIPPY_FOLDER / "lang"

PLUGINS_FOLDER = SKIPPY_FOLDER / "plugins"

if is_frozen():
    APPDATA_FOLDER = get_datadir()

    PROPERTY_FOLDER = APPDATA_FOLDER / "property"

    LOGS_FOLDER = APPDATA_FOLDER / "logs"

    PLUGINS_FOLDER = APPDATA_FOLDER / "plugins"

LOG_FILE = LOGS_FOLDER / f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log"
