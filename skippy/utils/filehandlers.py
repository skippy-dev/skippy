"""Various file handlers.
"""
import skippy.config

from typing import Optional, Tuple, Dict, Any
from abc import ABCMeta, abstractmethod
import pathlib
import json
import os


class AbstractFileHandler(metaclass=ABCMeta):

    """Abstract file handler

    Attributes:
        filepath (pathlib.Path): Path to handle file
    """

    _file: str

    def __init__(self, filepath: Optional[pathlib.Path] = None):
        """Init FileHandler

        Args:
            filepath (Optional[pathlib.Path], optional): Path to handle file
        """
        self.filepath = filepath or skippy.config.PROPERTY_FOLDER / self._file

    def read(self) -> str:
        """Read file

        Returns:
            str: File text
        """
        return self.filepath.read_text()

    def write(self, text: str):
        """Write file

        Args:
            text (str): File text
        """
        self.filepath.write_text(text)

    @abstractmethod
    def load(self):
        """Abstract load method"""
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        """Abstract save method"""
        pass


class ProfileHandler(AbstractFileHandler):

    """Profile handler

    Attributes:
        _file (str): Handled file name
    """

    _file = "profile.json"

    def load(self) -> Tuple[str, str]:
        """Load profile

        Returns:
            Tuple[str, str]: Tuple of user login and password
        """
        if os.path.exists(self.filepath) and self.read():
            profile = json.loads(self.read())
            return profile["login"], profile["password"]
        return "", ""

    def save(self, login: str, password: str):
        """Save profile

        Args:
            login (str): User login
            password (str): User password
        """
        data = {"login": login, "password": password}
        profile = json.dumps(data)

        self.write(profile)

    def logout(self):
        """Logout from account"""
        self.save("", "")


class SessionHandler(AbstractFileHandler):

    """Session Handler

    Attributes:
        _file (str): Handled file name
    """

    _file = "session.json"

    def load(self) -> Dict[str, Any]:
        """Load session

        Returns:
            Dict[str, Any]: Session
        """
        if os.path.exists(self.filepath) and self.read():
            return json.loads(self.read())
        return {"session": [], "pos": 0}

    def save(self, session: Dict[str, Any]):
        """Save session

        Args:
            session (Dict[str, Any]): Save session
        """
        self.write(json.dumps(session))
