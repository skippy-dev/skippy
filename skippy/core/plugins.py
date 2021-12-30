"""Plugin system core module
"""
from skippy.api import Singleton

from skippy.core.fields import AbstractField

from skippy.utils.logger import log

import skippy.config

from typing import Iterator, Optional, Callable, Union, Dict, List, Any
from abc import ABCMeta, abstractmethod
from pathlib import Path
import importlib
import toml
import sys

sys.path.append(skippy.config.PLUGINS_FOLDER.as_posix())


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


class PluginMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = super(PluginMeta, cls).__call__(*args, **kwargs)
        if hasattr(obj, "addField"):
            for key, value in type(obj).__dict__.items():
                if isinstance(value, AbstractField):
                    obj.addField(key, value)
        else:
            raise AttributeError(f"\"{cls.__name__}\" class has no method \"addField\"")
        return obj


class ABCPluginMeta(PluginMeta, ABCMeta):
    pass


class AbstractPlugin(metaclass=ABCPluginMeta):
    """Base plugin class"""

    __alias__: str

    __description__: str
    __author__: str
    __version__: str

    def __init__(self):
        self._settingsPath: Path = skippy.config.PLUGINS_FOLDER / f"{self.__alias__}.toml"
        self._fields: Dict[str, AbstractField] = {}

    def addField(self, name: str, setting: AbstractField):
        self._fields[name] = setting

    def load_settings(self):
        if self._fields and self._settingsPath.exists():
            with self._settingsPath.open() as f:
                settings = toml.load(f)
            for setting in settings:
                if setting in self._fields:
                    self._fields[setting].from_toml(settings[setting])

    def save_settings(self):
        if self._fields:
            with self._settingsPath.open("w") as f:
                toml.dump({setting: self._fields[setting].to_toml() for setting in self._fields}, f)

    @abstractmethod
    def start(self):
        """Abstract start method"""
        pass

    @abstractmethod
    def stop(self):
        """Abstract stop method"""
        pass


class PluginLoader(metaclass=Singleton):
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
        return [file.stem for file in skippy.config.PLUGINS_FOLDER.iterdir() if
                file.is_file() and file.name.endswith("_plugin.py")]

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
