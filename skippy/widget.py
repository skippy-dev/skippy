from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import collections
import requests
import hashlib
import base64
import json
import pyscp
import sys
import os

from skippy.utils.logger import log
import skippy.utils.critical
import skippy.utils.profile
import skippy.config


class ToolbarWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self = parent
        self.action_list = {}

        self.file_toolbar = QToolBar("File")
        self.file_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.file_toolbar)
        self.file_menu = self.menuBar().addMenu("&File")

        new_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "new.png",
                )
            ),
            "New",
            self,
        )
        self.action_list[new_action] = "new"
        new_action.setStatusTip("New")
        new_action.triggered.connect(lambda: self.tab.new_tab())
        self.file_menu.addAction(new_action)
        self.file_toolbar.addAction(new_action)

        open_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "open.png",
                )
            ),
            "Open",
            self,
        )
        self.action_list[open_action] = "open"
        open_action.setStatusTip("Open page")
        open_action.triggered.connect(self.download)
        self.file_menu.addAction(open_action)
        self.file_toolbar.addAction(open_action)

        upload_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "upload.png",
                )
            ),
            "Upload",
            self,
        )
        self.action_list[upload_action] = "upload"
        upload_action.setStatusTip("Upload page")
        upload_action.triggered.connect(
            lambda: self.upload(self.tab.tabs.currentWidget())
        )
        self.file_menu.addAction(upload_action)
        self.file_toolbar.addAction(upload_action)

        upload_as_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "upload_as.png",
                )
            ),
            "Upload as...",
            self,
        )
        self.action_list[upload_as_action] = "upload_as"
        upload_as_action.setStatusTip("Upload page as...")
        upload_as_action.triggered.connect(
            lambda: self.upload_as(self.tab.tabs.currentWidget())
        )
        self.file_menu.addAction(upload_as_action)
        self.file_toolbar.addAction(upload_as_action)

        close_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "close.png",
                )
            ),
            "Close",
            self,
        )
        self.action_list[close_action] = "close"
        close_action.setStatusTip("Close")
        close_action.triggered.connect(
            lambda: self.tab.remove_tab(self.tab.tabs.currentIndex())
        )
        self.file_menu.addAction(close_action)
        self.file_toolbar.addAction(close_action)

        self.file_menu.addSeparator()

        load_session_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "load_session.png",
                )
            ),
            "Load Session...",
            self,
        )
        self.action_list[load_session_action] = "load_session"
        load_session_action.setStatusTip("Load Session...")
        load_session_action.triggered.connect(self.load_session)
        self.file_menu.addAction(load_session_action)

        save_session_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "save_session.png",
                )
            ),
            "Save Session as...",
            self,
        )
        self.action_list[save_session_action] = "save_session"
        save_session_action.setStatusTip("Save Session as...")
        save_session_action.triggered.connect(self.save_session)
        self.file_menu.addAction(save_session_action)

        self.file_menu.addSeparator()

        exit_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "exit.png",
                )
            ),
            "Exit",
            self,
        )
        self.action_list[exit_action] = "exit"
        exit_action.setStatusTip("Exit")
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        self.edit_toolbar = QToolBar("Edit")
        self.edit_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.edit_toolbar)
        self.edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "undo.png",
                )
            ),
            "Undo",
            self,
        )
        self.action_list[undo_action] = "undo"
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).undo()
        )
        self.edit_toolbar.addAction(undo_action)
        self.edit_menu.addAction(undo_action)

        redo_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "redo.png",
                )
            ),
            "Redo",
            self,
        )
        self.action_list[redo_action] = "redo"
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).redo()
        )
        self.edit_toolbar.addAction(redo_action)
        self.edit_menu.addAction(redo_action)

        self.edit_menu.addSeparator()

        cut_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "cut.png",
                )
            ),
            "Cut",
            self,
        )
        self.action_list[cut_action] = "cut"
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).cut()
        )
        self.edit_toolbar.addAction(cut_action)
        self.edit_menu.addAction(cut_action)

        copy_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "copy.png",
                )
            ),
            "Copy",
            self,
        )
        self.action_list[copy_action] = "copy"
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).copy()
        )
        self.edit_toolbar.addAction(copy_action)
        self.edit_menu.addAction(copy_action)

        paste_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "paste.png",
                )
            ),
            "Paste",
            self,
        )
        self.action_list[paste_action] = "paste"
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).paste()
        )
        self.edit_toolbar.addAction(paste_action)
        self.edit_menu.addAction(paste_action)

        select_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "redo.png",
                )
            ),
            "Select all",
            self,
        )
        self.action_list[select_action] = "redo"
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(
            lambda: self.tab.tabs.currentWidget().findChild(QPlainTextEdit).selectAll()
        )
        self.edit_menu.addAction(select_action)

        self.settings_menu = self.menuBar().addMenu("&Settings")

        toggle_theme_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "toggle.png",
                )
            ),
            "Toggle Theme",
            self,
        )
        self.action_list[toggle_theme_action] = "toggle"
        toggle_theme_action.setStatusTip("Toggle Theme")
        toggle_theme_action.triggered.connect(self.toggle_theme)
        self.settings_menu.addAction(toggle_theme_action)

        self.settings_menu.addSeparator()

        login_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "login.png",
                )
            ),
            "Login",
            self,
        )
        self.action_list[login_action] = "login"
        login_action.setStatusTip("Login")
        login_action.triggered.connect(self.login)
        self.settings_menu.addAction(login_action)

        logout_action = QAction(
            QIcon(
                os.path.join(
                    skippy.config.ASSETS_FOLDER,
                    self.settings.value("mode", "light"),
                    "logout.png",
                )
            ),
            "Logout",
            self,
        )
        self.action_list[logout_action] = "logout"
        logout_action.setStatusTip("Logout")
        logout_action.triggered.connect(self.logout)
        self.settings_menu.addAction(logout_action)


class LoginStatusWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.setGeometry(300, 300, 300, 50)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("", self)
        self.label.setFont(QFont("Arial", 10))

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        username = skippy.utils.profile.Profile.load()[0]
        if username != "" and username != None:
            self.label.setText(f"Signed in as {username}")
        else:
            self.label.setText("")

    def set_text(self, text):
        self.label.setText(f"Signed in as {text}")


class ProjectList(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar{font-family: Arial; font-size:10pt;}")
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.resize(300, 200)
        self.setAcceptDrops(True)

        self.tabs.tabCloseRequested.connect(self.remove_tab)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.new_tab()

    @skippy.utils.critical.critical
    def new_tab(self, title="New Tab", source="", tags=[], files={}, parent=None):
        tab = QWidget()
        self.tabs.addTab(tab, title)
        tab.layout = QVBoxLayout(tab)

        if type(files) != dict:
            files = {}

        tab.data = {
            "title": title,
            "source": source,
            "tags": tags,
            "files": files,
            "parent": parent,
        }

        def setData(param, data):
            tab.data[param] = data

        title_box = FileUploadLineEdit()
        title_box.setText(title)
        title_box.textEdited.connect(
            lambda: self.tabs.setTabText(self.tabs.currentIndex(), title_box.text())
        )
        title_box.textEdited.connect(lambda text: setData("title", text))
        title_box.textEdited.connect(self.parent.update_title)
        title_box.setStyleSheet("QLineEdit{font-family: Arial; font-size:11pt;}")

        editor = FileUploadPlainEdit()
        editor.setPlainText(source)
        editor.textChanged.connect(lambda: setData("source", editor.toPlainText()))
        editor.setStyleSheet("QPlainTextEdit{font-family: Arial; font-size:11pt;}")

        tags_box = FileUploadLineEdit()
        if isinstance(tags, collections.Iterable):
            tags_box.setText(" ".join(tags))
        tags_box.textChanged.connect(lambda text: setData("tags", text.split(' ')))
        tags_box.setStyleSheet("QLineEdit{font-family: Arial; font-size:11pt;}")

        files_button = QPushButton("Files", self)
        files_button.clicked.connect(self.files_dialog)

        tab.layout.addWidget(title_box)
        tab.layout.addWidget(editor)
        tab.layout.addWidget(tags_box)
        tab.layout.addWidget(files_button)
        tab.setLayout(tab.layout)

        log.debug(f"New tab is created with title: {title}")

        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    @skippy.utils.critical.critical
    def remove_tab(self, index):
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.new_tab()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.dadDialog = DragAndDropWidget(self)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()
        self.dadDialog.close()

    def dropEvent(self, event):
        self.dadDialog.close()
        widget = self.tabs.currentWidget()
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.thread = QThread()
        self.worker = UploadFiles(files)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(self.upload_file)
        self.thread.start()

    def upload_file(self, file):
        filename = file[0]
        source = file[1]
        widget = self.tabs.currentWidget()
        widget.data["files"][filename] = (
            str(base64.b64encode(source)).replace("b'", "").replace("'", "")
        )

    def files_dialog(self):
        widget = self.tabs.currentWidget()
        fDialog = FilesDialog(widget, self)


class FileUploadLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(QLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.dadDialog = DragAndDropWidget(self)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()
        self.dadDialog.close()

    def dropEvent(self, event):
        self.dadDialog.close()


class FileUploadPlainEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(QPlainTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.dadDialog = DragAndDropWidget(self)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()
        self.dadDialog.close()

    def dropEvent(self, event):
        self.dadDialog.close()


class DragAndDropWidget(QWidget):
    CLOSE = pyqtSignal()

    def __init__(self, parent=None):
        super(DragAndDropWidget, self).__init__(parent)
        self.width, self.height = (
            parent.frameGeometry().width(),
            parent.frameGeometry().height(),
        )

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.popup_fillColor = QColor(240, 240, 240, 255)
        self.popup_penColor = QColor(200, 200, 200, 255)

        self.CLOSE.connect(self.close)

        self.move(0, 0)
        self.resize(self.width, self.height)
        self.show()

    def resizeEvent(self, event):
        popup_width = 300
        popup_height = 120
        ow = int(self.width / 2 - popup_width / 2)
        oh = int(self.height / 2 - popup_height / 2)

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, self.width, self.height)

        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)
        popup_width = 300
        popup_height = 120
        ow = int(self.width / 2 - popup_width / 2)
        oh = int(self.height / 2 - popup_height / 2)
        qp.drawRoundedRect(ow, oh, popup_width, popup_height, 5, 5)

        font = QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QColor(70, 70, 70))
        tolw, tolh = 80, -5
        qp.drawText(
            ow + int(popup_width / 2) - tolw,
            oh + int(popup_height / 2) - tolh,
            "Drop File.",
        )

        qp.end()

    def _close(self):
        self.CLOSE.emit()


class FilesDialog(QDialog):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Files list", self)
        self.label.setFont(QFont("Arial", 10))

        self.fileWidget = FilesWidget(widget, self)

        self.setLayout(self.layout)
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.fileWidget, alignment=Qt.AlignCenter)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(300, 300)
        self.resize(200, 100)
        self.show()


class FilesWidget(QWidget):
    def __init__(self, widget, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent

        self.layout = QGridLayout(self)

        files = widget.data["files"]

        pos = []
        for i in range(int(len(files) / 3)):
            for j in range(3):
                pos.append((i, j))
        if len(files) % 3 != 0:
            for i in range(len(files) % 3):
                pos.append((int(len(files) / 3), i))

        for e, p in zip(list(files.keys()), pos):
            self.layout.addWidget(FileWidget(e, widget, self), p[0], p[1])

        self.setLayout(self.layout)


class FileWidget(QWidget):
    del_widget = pyqtSignal(str)

    def __init__(self, title, widget, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.widget = widget
        # self.setStyleSheet('background-color: rgb(225,225,225); margin:5px; border:1px solid rgb(0, 0, 0);')

        self.title = title

        self.layout = QGridLayout(self)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(title)
        self.lineEdit.setFixedSize(200, 40)
        self.lineEdit.textEdited.connect(self.set_title)

        self.remove_button = QPushButton("X", self)
        self.remove_button.clicked.connect(self.remove_file)

        self.layout.addWidget(self.lineEdit, 0, 0)
        self.layout.addWidget(self.remove_button, 0, 1)
        self.setLayout(self.layout)

    @skippy.utils.critical.critical
    def set_title(self, text):
        self.widget.data["files"][text] = self.widget.data["files"][self.title]
        log.debug(f"file ")
        del self.widget.data["files"][self.title]
        self.title = text

    @skippy.utils.critical.critical
    def remove_file(self, *args):
        self.widget.data["files"].pop(self.title)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.auth = False

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Sign in to your Wikidot account", self)
        self.login_box = QLineEdit()
        self.login_box.setPlaceholderText("Login")
        self.password_box = QLineEdit()
        self.password_box.setEchoMode(QLineEdit.Password)
        self.password_box.setPlaceholderText("Password")
        self.button = QPushButton("Ok", self)

        self.button.clicked.connect(self.login)

        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.login_box)
        self.layout.addWidget(self.password_box)
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(300, 300)
        self.resize(200, 100)
        self.show()

    def login(self):
        login = self.login_box.text()
        password = self.password_box.text()
        skippy.utils.profile.Profile.save(login, password)
        self.parent.show()
        self.auth = True
        log.debug(f"Login as {login}")
        self.parent.login_status.set_text(login)
        self.close()

    def closeEvent(self, event):
        if not self.auth:
            sys.exit()


class UploadDialog(QDialog):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.layout = QVBoxLayout(self)

        self.sites = {}

        def addSites(sites):
            if sites[0] in self.sites:
                addSites((sites[0] + "(1)", sites[1]))
            else:
                self.sites[sites[0]] = sites[1]
                self.site_box.addItem(sites[0])

        self.label = QLabel("Enter page url", self)
        self.site_box = QComboBox(self)
        self.thread = QThread()
        self.worker = GetSites()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(addSites)
        self.page_box = QLineEdit()
        self.page_box.setPlaceholderText("Page name")
        self.comment_box = QLineEdit()
        self.comment_box.setText("Edit using Skippy")
        self.comment_box.setPlaceholderText("Comment")
        self.button = QPushButton("Ok", self)

        self.button.clicked.connect(self.upload)

        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.site_box)
        self.layout.addWidget(self.page_box)
        self.layout.addWidget(self.comment_box)
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(300, 300)
        self.resize(200, 100)

        self.thread.start()
        self.show()

    @skippy.utils.critical.critical
    def upload(self, *args):
        site = str(self.site_box.currentText())
        page = self.page_box.text()
        comment = self.comment_box.text()
        wiki = self.sites[site]
        profile = skippy.utils.profile.Profile.load()
        wiki.auth(profile[0], profile[1])
        p = wiki(page)
        p.edit(
            source=self.widget.data["source"],
            title=self.widget.data["title"],
            comment=comment,
        )
        self.widget.data["parent"] = [
            self.sites[site].site.replace("http://", ""),
            page,
        ]
        p.set_tags(self.widget.data["tags"])

        for file in self.widget.data["files"]:
            p.upload(file, base64.b64decode(self.widget.data["files"][file]))
            log.debug(f"File {file} is uploaded")
        for file in p.files:
            if file.name not in self.widget.data["files"]:
                p.remove_file(file.name)
                log.debug(f"File {file.name} is deleted")
        log.debug(
            f"""Upload "{self.widget.data["title"]}" to "{"/".join(self.widget.data["parent"])}" """
        )
        self.close()

    def closeEvent(self, e):
        self.worker.stop()
        e.accept()


class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.sites = {}

        def addSites(sites):
            if sites[0] in self.sites:
                addSites((sites[0] + "(1)", sites[1]))
            else:
                self.sites[sites[0]] = sites[1]
                self.site_box.addItem(sites[0])

        self.label = QLabel("Enter page url", self)
        self.site_box = QComboBox(self)
        self.thread = QThread()
        self.worker = GetSites()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(addSites)
        self.page_box = QLineEdit()
        self.page_box.setPlaceholderText("Page name")
        self.button = QPushButton("Ok", self)

        self.button.clicked.connect(self.download)

        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.site_box)
        self.layout.addWidget(self.page_box)
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(300, 300)
        self.resize(200, 100)

        self.thread.start()
        self.show()

    @skippy.utils.critical.critical
    def download(self, *args):
        site = str(self.site_box.currentText())
        page = self.page_box.text()

        wiki = self.sites[site]
        p = wiki(page)

        url = [self.sites[site].site.replace("http://", ""), page]

        files = {}
        for i in p.files:
            with requests.get(i.url) as res:
                files[i.name] = (
                    str(base64.b64encode(res.content))
                    .replace("b'", "")
                    .replace("'", "")
                )

        self.parent.tab.new_tab(p.title, p.source, list(p.tags), files, url)
        log.debug(f"""Download page from "{self.sites[site].site}" """)
        self.close()

    def closeEvent(self, e):
        self.worker.stop()
        e.accept()


class GetSites(QObject):
    progress = pyqtSignal(tuple)
    finished = pyqtSignal()
    cache = []
    run = True

    def run(self):
        sites = pyscp.wikidot.User(skippy.utils.profile.Profile.load()[0]).member
        for data in self.cache:
            self.progress.emit((data[0], data[1]))
        if len(self.cache) < len(sites):
            for site in sites[len(self.cache) :]:
                if self.run:
                    self.progress.emit((site.title, site))
                    self.cache.append((site.title, site))
                    log.debug(f"Get sites: {site.title}")
        self.finished.emit()

    def stop(self):
        self.run = False


class UploadFiles(QObject):
    progress = pyqtSignal(tuple)
    finished = pyqtSignal()

    def __init__(self, files):
        super(UploadFiles, self).__init__()
        self.files = files

    def run(self):
        log.debug("File loaded started...")
        for file in self.files:
            if os.path.isfile(file):
                filename = os.path.basename(file)
                with open(file, "rb") as f:
                    source = f.read()
                log.debug(f"Load {file}")
                self.progress.emit((filename, source))
        self.finished.emit()
