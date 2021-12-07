"""Translator
"""
from skippy.api import Singleton, Language
import skippy.config

from typing import List
import toml
import os


class Translator(metaclass=Singleton):

    """Translator class"""

    def __init__(self):
        """Init translator class"""
        self._language = None

    @staticmethod
    def languages() -> List[str]:
        """Get all exist skippy languages

        Returns:
            List[str]: List of languages code
        """
        return [
            os.path.splitext(file)[0]
            for file in os.listdir(skippy.config.LANG_FOLDER)
            if os.path.isfile(os.path.join(skippy.config.LANG_FOLDER, file))
            if os.path.splitext(file)[1] == ".toml"
        ]

    @staticmethod
    def getLangName(lang: str) -> str:
        """Get lang name by code

        Args:
            lang (str): Language code

        Returns:
            str: Language name
        """
        path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.toml")
        with open(path, encoding="utf-8") as f:
            return toml.load(f)["LANGUAGE"]

    def load(self, lang: str = "en") -> Language:
        """Load language by code

        Args:
            lang (str, optional): Language code

        Returns:
            Language: Language namedtuple, with language code and dictionary
        """
        path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.toml")
        with open(path, encoding="utf-8") as f:
            dictionary = toml.load(f)
        self._language = Language(lang, dictionary)

        return self._language

    def translate(self, context: str) -> str:
        """Translate context text

        Args:
            context (str): Text context

        Returns:
            str: Translated string if available, else return input context
        """
        try:
            out = self._language.dictionary
            for text in context.split("."):
                out = out[text]
            return out
        except KeyError:
            return context
