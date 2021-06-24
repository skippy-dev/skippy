from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qtmodern.styles
import collections

from skippy.utils.language import Translator
from skippy.utils.logger import log
import skippy.utils.critical
import skippy.utils.session
import skippy.utils.profile
import skippy.config
from skippy.widgets import *

import base64
import pyscp
import json
import os
import sys


class App(QMainWindow):
	def __init__(self, app):
		super(App, self).__init__()
		self.app = app

		self.settings = QSettings("skippy", "skippy")

		Translator.load(self.settings.value("lang", "en"))

		self.tab = ProjectList(self)
		self.tab.tabs.currentChanged.connect(self.update_title)

		self.session = skippy.utils.session.Session(self)
		self.session.load()

		self.menus = MenusWidget(self)

		self.login_status = LoginStatusWidget(self)
		self.login_status.move(500, -14)

		self.setCentralWidget(self.tab)

		self.status = QStatusBar()
		self.setStatusBar(self.status)

		self.update_title()
		self.setWindowIcon(
			QIcon(os.path.join(skippy.config.ASSETS_FOLDER, "skippy.ico"))
		)
		self.resize(self.settings.value("size", QSize(700, 700)))
		self.move(self.settings.value("pos", QPoint(200, 200)))
		self.setWindowState(
			Qt.WindowState(self.settings.value("state", Qt.WindowNoState))
		)
		self.font = QFont("Arial", 10)
		self.setFont(self.font)

	def update_title(self):
		self.setWindowTitle(
			f"{self.tab.tabs.tabText(self.tab.tabs.currentIndex())} | skippy - {skippy.config.version}"
		)

	@skippy.utils.critical.critical
	def download(self, *args):
		dDialog = DownloadDialog(self)

	@skippy.utils.critical.critical
	def upload(self, widget):
		if widget.data["parent"] != None:
			wiki = pyscp.wikidot.Wiki(widget.data["parent"][0])
			profile = skippy.utils.profile.Profile.load()
			wiki.auth(profile[0], profile[1])
			p = wiki(widget.data["parent"][1])
			p.edit(
				source=widget.data["source"],
				title=widget.data["title"],
				comment="Edit using Skippy",
			)
			p.set_tags(widget.data["tags"])
			for file in widget.data["files"]:
				try:
					p.upload(file, base64.b64decode(widget.data["files"][file]))
					log.debug(f"File {file} is uploaded")
				except RuntimeError as e:
					log.debug(f"RuntimeError({str(e)}): File {file} isn't uploaded")
			for file in p.files:
				if file.name not in widget.data["files"]:
					p.remove_file(file.name)
					log.debug(f"File {file.name} is deleted")
			log.debug(
				f"""Upload "{widget.data['title']}" to "{"/".join(widget.data["parent"])}" """
			)
		else:
			self.upload_as(widget)

	@skippy.utils.critical.critical
	def upload_as(self, widget):
		uDialog = UploadDialog(widget, self)

	@skippy.utils.critical.critical
	def login(self, *args):
		lDialog = LoginDialog(self)

	@skippy.utils.critical.critical
	def logout(self, *args):
		skippy.utils.profile.Profile.save("", "")
		self.hide()
		lDialod = LoginDialog(self)
		log.debug(f"Logout")

	@skippy.utils.critical.critical
	def save_session(self, *args):
		path, _ = QFileDialog.getSaveFileName(
			self, "Save file", "", "JSON file (*.json)\nAll files (*.*)"
		)
		if path != "":
			self.session.save(path)

	@skippy.utils.critical.critical
	def load_session(self, *args):
		path, _ = QFileDialog.getOpenFileName(
			self, "Save file", "", "JSON file (*.json)\nAll files (*.*)"
		)
		if path != "":
			self.session.load(path)
		self.session.save()

	@skippy.utils.critical.critical
	def toggle_theme(self, *args):
		if self.settings.value("mode", "light") == "light":
			log.debug("Dark mode now")
			self.settings.setValue("mode", "dark")
			qtmodern.styles.dark(self.app)
		else:
			log.debug("Light mode now")
			self.settings.setValue("mode", "light")
			qtmodern.styles.light(self.app)
		for i in self.menus.action_list:
			i.setIcon(
				QIcon(
					os.path.join(
						skippy.config.ASSETS_FOLDER,
						self.settings.value("mode", "light"),
						f"{self.menus.action_list[i]}.png",
					)
				)
			)

	def updateTranslate(self, lang):
		self.settings.setValue("lang", lang)
		self.restart()

	def restart(self):
		self.close()
		self.__class__(self.app).show()

	def contextMenuEvent(self, event):
		self.menus.contextMenu.exec_(self.mapToGlobal(event.pos()))

	def resizeEvent(self, event):
		self.login_status.move(self.width() - 200, -14)
		if self.width() < 350:
			self.login_status.hide()
		else:
			self.login_status.show()

	def closeEvent(self, e):
		self.settings.setValue("size", self.size())
		self.settings.setValue("pos", self.pos())
		self.settings.setValue("state", self.windowState())

		e.accept()


def start_ui():
	app = QApplication(sys.argv)
	app.setApplicationName("skippy")

	window = App(app)

	if window.settings.value("mode", "light") == "dark":
		qtmodern.styles.dark(app)
	else:
		qtmodern.styles.light(app)

	if (
		skippy.utils.profile.Profile.load()[0] == ""
		or skippy.utils.profile.Profile.load()[1] == ""
	):
		lDialod = LoginDialog(window)
	else:
		window.show()

	log.info("Skippy was started...")

	app.exec_()
	window.session.save()
