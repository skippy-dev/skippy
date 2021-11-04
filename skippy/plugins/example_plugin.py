"""Example plugin
"""
from skippy.core.plugins import BasePlugin
from skippy.utils.logger import log


class ExamplePlugin(BasePlugin):

    """This is a Example plugin class
    """
    
    __alias__ = "ExamplePlugin"

    __description__ = "I am a example plugin."
    __author__ = "MrNereof"
    __version__ = "1.0.0"

    def start(self):
        """do something on start
        """
        log.debug("Start")

    def stop(self):
        """do something on stop
        """
        log.debug("Stop")


def load() -> ExamplePlugin:
    """Load ExamplePlugin class
    
    Returns:
        ExamplePlugin: A ExamplePlugin instance
    """
    return ExamplePlugin()
