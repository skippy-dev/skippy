from skippy.utils.plugin import PluginBase
from skippy.utils.logger import log

class Plugin(PluginBase):
    __alias__ = "ExamplePlugin"

    __description__ = "I am a example plugin."
    __author__ = "MrNereof"
    __version__ = "1.0.0"

    def proccess(self):
        """do something"""
        log.debug(f"{self.__alias__}: {self.__description__}")
