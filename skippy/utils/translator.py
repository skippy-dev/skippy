"""Translator
"""
from skippy.api import Singleton, Language
import skippy.config

from typing import MutableMapping, List, Any
import toml


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
        return [file.stem for file in skippy.config.LANG_FOLDER.iterdir() if file.is_file() and file.suffix == ".toml"]

    @staticmethod
    def get_dictionary(lang: str) -> MutableMapping[str, Any]:
        """Get translation dictionary by lang code

        Args:
            lang (str): Language code

        Returns:
            MutableMapping[str, Any]: Dictionary
        """
        path = skippy.config.LANG_FOLDER / f"{lang}.toml"
        with path.open(encoding="utf-8") as f:
            return toml.load(f)

    @classmethod
    def get_lang_name(cls, lang: str) -> str:
        """Get lang name by code

        Args:
            lang (str): Language code

        Returns:
            str: Language name
        """
        return cls.get_dictionary(lang)["LANGUAGE"]

    def load(self, lang: str = "en") -> Language:
        """Load language by code

        Args:
            lang (str, optional): Language code

        Returns:
            Language: Language namedtuple, with language code and dictionary
        """
        dictionary = self.get_dictionary(lang)
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
