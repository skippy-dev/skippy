"""Autoupdater classes
"""
from skippy.api import ignore

from skippy.utils import cached_property, is_frozen

import skippy.config

from typing import Tuple, Union, List, Dict, Any
from abc import ABCMeta, abstractmethod
import requests


RequestException = requests.exceptions.RequestException


def version2tuple(version: str) -> Tuple[int]:
    """Convert string version to tuple

    Args:
        version (str): String version

    Returns:
        Tuple[int]: Tuple version
    """
    return tuple(map(int, version.split(".")))


class AbstractUpdateClient(metaclass=ABCMeta):

    """Abstract update client"""

    _apiEndpoint: str

    @staticmethod
    def getClient() -> "AbstractUpdateClient":
        """Get update client for Skippy

        Returns:
            AbstractUpdateClient: Update client
        """
        if is_frozen():
            return GithubReleasesClient()
        return PyPIClient()

    @cached_property
    @ignore(RequestException, {})
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
        """Abstract version property"""
        pass

    @abstractmethod
    def update(self):
        """Abstract update method"""
        pass


class PyPIClient(AbstractUpdateClient):

    """PyPI update client"""

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
        """Update method"""
        import os

        os.system("start cmd /c python -m pip install skippy-pad -U")


class GithubReleasesClient(AbstractUpdateClient):

    """Github releases client"""

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
        """Update method"""
        import webbrowser

        webbrowser.open(self.data["html_url"])
