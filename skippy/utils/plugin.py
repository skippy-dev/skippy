from abc import ABCMeta, abstractmethod
from PyQt5.QtWidgets import *
import sys
import os

from skippy.utils.logger import log
import skippy.config

class PluginBase(metaclass=ABCMeta):
    __alias__ = "Plugin"

    __description__ = ""
    __author__ = ""
    __version__ = "1.0.0"

    @abstractmethod
    def proccess(self):
        pass

class PluginLoader:
    def __init__(self):
        log.debug("Initializing plugin loader..")
        self.plugins = []

        self.load()
        log.debug("Initializing plugin loader finished")

    @staticmethod
    def files():
        return [
            os.path.splitext(f)[0]
            for f in os.listdir(skippy.config.PLUGINS_FOLDER)
            if os.path.isfile(os.path.join(skippy.config.PLUGINS_FOLDER, f))
            if os.path.splitext(f)[1] == ".py"
        ]

    @staticmethod
    def plugins_data():
        plugins_data = []
        for file in PluginLoader.files():
            plugin = __import__(file).Plugin
            plugins_data.append({'__alias__': plugin.__alias__, '__description__': plugin.__description__, '__author__': plugin.__author__, '__version__': plugin.__version__})
        return plugins_data

    def load(self):
        sys.path.append(skippy.config.PLUGINS_FOLDER)
        for file in self.files():
            plugin = __import__(file).Plugin()
            log.debug(f"Loading plugin {plugin.__alias__}..")
            self.plugins.append(plugin)
            plugin.proccess()
            log.debug(f"Plugin {plugin.__alias__} was loaded")
