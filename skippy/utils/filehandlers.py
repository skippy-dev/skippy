"""Various file handlers.
"""
import skippy.config

from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple, Dict, Any
import json
import os


class AbstractFileHandler(metaclass=ABCMeta):

    """Abstract file handler
    
    Attributes:
        filepath (str): Path to handle file
    """

    file: str

    def __init__(self, filepath: Optional[str] = None):
        """Init FileHandler
        
        Args:
            filepath (Optional[str], optional): Path to handle file
        """
        self.filepath = (
            filepath
            if filepath
            else os.path.join(skippy.config.PROPERTY_FOLDER, self.file)
        )

    def read(self) -> str:
        """Read file
        
        Returns:
            str: File text
        """
        with open(self.filepath, "r") as file:
            return file.read()

    def write(self, text: str):
        """Write file
        
        Args:
            text (str): File text
        """
        with open(self.filepath, "w") as file:
            file.write(text)

    @abstractmethod
    def load(self):
        """Abstract load method
        """
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        """Abstract save method
        """
        pass


class ProfileHandler(AbstractFileHandler):

    """Profile handler
    
    Attributes:
        file (str): Handled file name
    """

    file = "profile.json"

    def load(self) -> Tuple[str, str]:
        """Load profile
        
        Returns:
            Tuple[str, str]: Tuple of user login and password
        """
        if os.path.exists(self.filepath) and self.read():
            profile = json.loads(self.read())
            return (profile["login"], profile["password"])
        return ("", "")

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
        """Logout from account
        """
        self.save("", "")


class SessionHandler(AbstractFileHandler):

    """Session Handler
    
    Attributes:
        file (str): Handled file name
    """

    file = "session.json"

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
