import skippy

import os
import json

version = skippy.__version__

SKIPPY_FOLDER = os.path.dirname(os.path.realpath(__file__))

ASSETS_FOLDER = os.path.join(SKIPPY_FOLDER, "assets")

PROPERTY_FOLDER = os.path.join(SKIPPY_FOLDER, "property")

LOGS_FOLDER = os.path.join(SKIPPY_FOLDER, "logs")

LANG_FOLDER = os.path.join(SKIPPY_FOLDER, "lang")

PLUGINS_FOLDER = os.path.join(SKIPPY_FOLDER, "plugins")
