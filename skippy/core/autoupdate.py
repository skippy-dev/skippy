"""Autoupdater classes
"""
from skippy.api import ConnectionErrors, ignore

import skippy.config

from typing import Callable, Tuple, Union, List, Dict, Any
from abc import ABCMeta, abstractmethod
import requests
import sys

try:
    from functools import cached_property
except ImportError:
    from functools import lru_cache

    def cached_property(func: Callable[[None], Any]) -> property:
        """Cached property
        
        Args:
            func (Callable[[None], Any]): Property method
        
        Returns:
            property: Property instance
        """
        return property(lru_cache(func))


def version2tuple(version: str) -> Tuple[int]:
    """Convert string version to tuple
    
    Args:
        version (str): String version
    
    Returns:
        Tuple[int]: Tuple version
    """
    return tuple(map(int, version.split(".")))


def isFrozen() -> bool:
    """Is Skippy compiled to exe
    
    Returns:
        bool: Compiled or not
    """
    return getattr(sys, "frozen", False)


class AbstractUpdateClient(metaclass=ABCMeta):

    """Abstract update client
    """
    
    _apiEndpoint: str

    @staticmethod
    def getClient() -> "AbstractUpdateClient":
        """Get update client for Skippy
        
        Returns:
            AbstractUpdateClient: Update client
        """
        if isFrozen():
            return GithubReleasesClient()
        return PyPIClient()

    @cached_property
    @ignore(ConnectionErrors, {})
    def data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Update data property
        
        Returns:
            Dict[str, Any]: Update data
        """
        response = requests.get(self._apiEndpoint)
        return response.json()

    def checkVersion(self) -> bool:
        """Check if Skippy has a new version
        
        Returns:
            bool: Is new version available
        """
        return not version2tuple(skippy.config.version) >= version2tuple(self.version)

    @property
    @abstractmethod
    def version(self):
        """Abstract version property
        """
        pass

    @abstractmethod
    def update(self):
        """Abstract update method
        """
        pass


class PyPIClient(AbstractUpdateClient):

    """PyPI update client
    """
    
    _apiEndpoint = "https://pypi.org/pypi/skippy-pad/json"

    @property
    @ignore(KeyError, "0.0.0")
    def version(self) -> str:
        """Update version property
        
        Returns:
            str: Version
        """
        return self.data["info"]["version"]

    def update(self):
        """Update method
        """
        import os

        os.system("start cmd /c python -m pip install skippy-pad -U")


class GithubReleasesClient(AbstractUpdateClient):

    """Github releases client
    """
    
    _apiEndpoint = "https://api.github.com/repos/skippy-dev/skippy/releases"

    @property
    @ignore(KeyError, {})
    def data(self) -> Dict[str, Any]:
        """Update data property
        
        Returns:
            Dict[str, Any]: Update data
        """
        return super().data[0]

    @property
    @ignore(KeyError, "0.0.0")
    def version(self) -> str:
        """Update version property
        
        Returns:
            str: Version
        """
        return self.data["tag_name"][1:]

    def update(self):
        """Update method
        """
        import webbrowser

        webbrowser.open(self.data["html_url"])
