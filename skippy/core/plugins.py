"""Plugin system core module
"""
from skippy.utils.logger import log

import skippy.config

from typing import Iterator, Optional, Callable, Union, Dict, Any
import importlib
import sys
import os

sys.path.append(skippy.config.PLUGINS_FOLDER)


def inject(
    module: str, attr: str, value: Optional[Any] = None
) -> Union[Any, Callable[[Any], Any]]:
    """Inject value into selected module attribute.

    Note: This function is not safe. It can be used only in plugins for injecting variable into skippy source code.

    Args:
        module (str): Module name
        attr (str): Attribute name
        value (Optional[Any], optional): Any value or None (if None func return decorator wrapper)

    Returns:
        Union[Any, Callable[Any]]: If value is not None return value, else return decorator wrapper
    """

    def inject(value: Any) -> Any:
        """Inject value into selected module attribute.

        Args:
            value (Any): Any value

        Returns:
            Any: Input value
        """
        loc = {}
        exec(f"import {module}; module = {module}", globals(), loc)
        setattr(loc["module"], attr, value)

        return value

    return inject(value) if value else inject


class BasePlugin:

    """Base plugin class"""

    __alias__ = "Plugin"

    __description__ = ""
    __author__ = ""
    __version__ = "1.0.0"

    def start(self):
        """Base start method"""
        pass

    def stop(self):
        """Base stop method"""
        pass


class PluginLoader:

    """Plugin loader class"""

    def __init__(self):
        """Init Plugin loader"""
        self._plugins = []

    @staticmethod
    def plugins() -> list:
        """Get list of all plugins

        Returns:
            list: List of plugins
        """
        return [
            os.path.splitext(file)[0]
            for file in os.listdir(skippy.config.PLUGINS_FOLDER)
            if os.path.isfile(os.path.join(skippy.config.PLUGINS_FOLDER, file))
            if file.endswith("_plugin.py")
        ]

    @classmethod
    def pluginsData(cls) -> Iterator[Dict[str, str]]:
        """Get data of all plugins

        Yields:
            Dict[str, str]: Dict of plugin data
        """
        for file in cls.plugins():
            plugin = cls.importPlugin(file)
            yield {
                "__alias__": plugin.__alias__,
                "__description__": plugin.__description__,
                "__author__": plugin.__author__,
                "__version__": plugin.__version__,
            }

    def loadPlugins(self):
        """Load all plugins"""
        for file in self.plugins():
            plugin = self.importPlugin(file)
            self._plugins.append(plugin)

    def startPlugins(self):
        """Start all plugins"""
        for plugin in self._plugins:
            plugin.start()
            log.debug(f"{plugin.__alias__} was started")

    def stopPlugins(self):
        """Stop all plugins"""
        for plugin in self._plugins:
            plugin.stop()
            log.debug(f"{plugin.__alias__} was stoped")

    @staticmethod
    def importPlugin(module: str) -> BasePlugin:
        """Import plugin by module name

        Args:
            module (str): Module name

        Returns:
            BasePlugin: Plugin instance
        """
        return importlib.import_module(module).load()
