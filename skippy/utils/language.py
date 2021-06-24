import skippy.config

import json
import os
try:
	from collections.abc import namedtuple
except ImportError:
	from collections import namedtuple

Language = namedtuple("Language","code dict")

class Translator:
	language = None

	@staticmethod
	def languages():
		return [
			os.path.splitext(file)[0]
			for file in os.listdir(skippy.config.LANG_FOLDER)
			if os.path.isfile(os.path.join(skippy.config.LANG_FOLDER, file))
			if os.path.splitext(file)[1] == ".json"
		]

	@staticmethod
	def getLangName(lang):
		path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.json")
		with open(path, encoding='utf-8') as f:
			return json.loads(f.read())["LANGUAGE"]

	@classmethod
	def load(cls, lang="en"):
		path = os.path.join(skippy.config.LANG_FOLDER, f"{lang}.json")
		with open(path, encoding='utf-8') as f:
			dictionary = json.loads(f.read())
		cls.language = Language(lang,dictionary)

		return cls.language

	@classmethod
	def translate(cls, context):
		try:
			return cls.language.dict[context]
		except KeyError:
			return context