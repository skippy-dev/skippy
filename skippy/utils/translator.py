"""Translator
"""
from skippy.api import Singleton, Language
import skippy.config

from typing import List
import json
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
            if os.path.splitext(file)[1] == ".json"
        ]

    @staticmethod
    def getLangName(lang: str) -> str:
        """Get lang name by code

        Args:
            lang (str): Language code

        Returns:
            str: Language name
        """
        path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.json")
        with open(path, encoding="utf-8") as f:
            return json.loads(f.read())["LANGUAGE"]

    def load(self, lang: str = "en") -> Language:
        """Load language by code

        Args:
            lang (str, optional): Language code

        Returns:
            Language: Language namedtuple, with language code and dictionary
        """
        path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.json")
        with open(path, encoding="utf-8") as f:
            dictionary = json.loads(f.read())
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
            return self._language.dictionary[context]
        except KeyError:
            return context
