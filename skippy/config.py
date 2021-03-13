import os
import json

import skippy

version = skippy.__version__

SKIPPY_FOLDER = os.path.dirname(os.path.realpath(__file__))

ASSETS_FOLDER = os.path.join(SKIPPY_FOLDER, 'assets')

PROPERTY_FOLDER = os.path.join(SKIPPY_FOLDER, 'property')

LOGS_FOLDER = os.path.join(SKIPPY_FOLDER, 'logs')

PLUGINS_FOLDER = os.path.join(SKIPPY_FOLDER, 'plugins')

with open(os.path.join(PROPERTY_FOLDER, 'settings.json'), 'r') as f:
    settings = json.loads(f.read())