"""Plugin system core module
"""
from skippy.core.settings import AbstractSetting

from skippy.utils.logger import log

import skippy.config

from typing import Iterator, Optional, Callable, Union, Dict, List, Any
from abc import ABCMeta, abstractmethod
import importlib
import toml
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


class AbstractPlugin(metaclass=ABCMeta):

    """Base plugin class"""

    __alias__: str

    __description__: str
    __author__: str
    __version__: str

    def __init__(self):
        self._settingsPath: str = os.path.join(
            skippy.config.PLUGINS_SETTINGS_FOLDER, f"{self.__alias__}.toml"
        )
        self._settings: Dict[str, AbstractSetting] = {}

    def addSetting(self, name: str, setting: AbstractSetting):
        self._settings[name] = setting

    def load_settings(self):
        if self._settings and os.path.exists(self._settingsPath):
            with open(self._settingsPath) as f:
                settings = toml.load(f)
            for setting in settings:
                if setting in self._settings:
                    self._settings[setting].from_toml(settings[setting])

    def save_settings(self):
        if self._settings:
            with open(self._settingsPath, "w") as f:
                toml.dump(
                    {
                        setting: self._settings[setting].to_toml()
                        for setting in self._settings
                    },
                    f,
                )

    @abstractmethod
    def start(self):
        """Abstract start method"""
        pass

    @abstractmethod
    def stop(self):
        """Abstract stop method"""
        pass


class PluginLoader:

    """Plugin loader class"""

    def __init__(self):
        """Init Plugin loader"""
        self._plugins: List[AbstractPlugin] = []

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
    def plugins_data(cls) -> Iterator[Dict[str, str]]:
        """Get data of all plugins

        Yields:
            Dict[str, str]: Dict of plugin data
        """
        for file in cls.plugins():
            plugin = cls.import_plugin(file)
            yield {
                "__alias__": plugin.__alias__,
                "__description__": plugin.__description__,
                "__author__": plugin.__author__,
                "__version__": plugin.__version__,
            }

    def load_plugins(self):
        """Load all plugins"""
        for file in self.plugins():
            plugin = self.import_plugin(file)
            self._plugins.append(plugin)

    def start_plugins(self):
        """Start all plugins"""
        for plugin in self._plugins:
            plugin.load_settings()
            plugin.start()
            log.debug(f"{plugin.__alias__} was started")

    def stop_plugins(self):
        """Stop all plugins"""
        for plugin in self._plugins:
            plugin.stop()
            plugin.save_settings()
            log.debug(f"{plugin.__alias__} was stoped")

    @staticmethod
    def import_plugin(module: str) -> AbstractPlugin:
        """Import plugin by module name

        Args:
            module (str): Module name

        Returns:
            AbstractPlugin: Plugin instance
        """
        return importlib.import_module(module).load()
