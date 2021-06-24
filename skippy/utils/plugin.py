from abc import ABCMeta, abstractmethod
from PyQt5.QtWidgets import *
import importlib
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
    def process(self):
        pass


class PluginLoader:
    def __init__(self):
        log.debug("Initializing plugin loader..")
        self.plugins = []

        self.load()
        log.debug("Initializing plugin loader finished")

    @staticmethod
    def modules():
        return [
            os.path.splitext(file)[0]
            for file in os.listdir(skippy.config.PLUGINS_FOLDER)
            if os.path.isfile(os.path.join(skippy.config.PLUGINS_FOLDER, file))
            if os.path.splitext(file)[1] == ".py"
        ]

    @classmethod
    def plugins_data(cls):
        plugins_data = []
        for file in cls.modules():
            plugin = cls.importPlugin(file)
            plugins_data.append(
                {
                    "__alias__": plugin.__alias__,
                    "__description__": plugin.__description__,
                    "__author__": plugin.__author__,
                    "__version__": plugin.__version__,
                }
            )
        return plugins_data

    def load(self):
        sys.path.append(skippy.config.PLUGINS_FOLDER)
        for file in self.modules():
            plugin = self.importPlugin(file)()
            log.debug(f"Loading plugin {plugin.__alias__}..")
            self.plugins.append(plugin)
            plugin.process()
            log.debug(f"Plugin {plugin.__alias__} was loaded")

    @staticmethod
    def importPlugin(file):
        return importlib.import_module(file).Plugin