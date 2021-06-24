from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functools import partial
import collections
import requests
import hashlib
import base64
import json
import pyscp
import sys
import os

from skippy.utils.language import Translator
from skippy.utils.preview import Preview
from skippy.utils.logger import log
import skippy.utils.critical
import skippy.utils.elements
import skippy.utils.profile
import skippy.config


class MenusWidget(QWidget):
    def __init__(self, parent=None):
        super(MenusWidget, self).__init__(parent)
        self.parent = parent
        menuBar = parent.menuBar()

        self.action_list = {}

        self.contextMenu = self.addMenu()

        file_menu = self.addMenu(Translator.translate("MENU_BAR_FILE_MENU"), menuBar)
        file_toolbar = self.addToolbar(Translator.translate("MENU_BAR_FILE_TOOLBAR"))

        self.addAction(
            Translator.translate("MENU_BAR_NEW_ACTION_NAME"),
            Translator.translate("MENU_BAR_NEW_ACTION_STATUS_TIP"),
            lambda: parent.tab.new_tab(),
            "new",
            file_menu,
            file_toolbar,
            self.contextMenu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_OPEN_ACTION_NAME"),
            Translator.translate("MENU_BAR_OPEN_ACTION_STATUS_TIP"),
            parent.download,
            "open",
            file_menu,
            file_toolbar,
        )
        self.addAction(
            Translator.translate("MENU_BAR_UPLOAD_ACTION_NAME"),
            Translator.translate("MENU_BAR_UPLOAD_ACTION_STATUS_TIP"),
            lambda: parent.upload(parent.tab.tabs.currentWidget()),
            "upload",
            file_menu,
            file_toolbar,
        )
        self.addAction(
            Translator.translate("MENU_BAR_UPLOAD_AS_ACTION_NAME"),
            Translator.translate("MENU_BAR_UPLOAD_AS_ACTION_STATUS_TIP"),
            lambda: parent.upload_as(parent.tab.tabs.currentWidget()),
            "upload_as",
            file_menu,
            file_toolbar,
        )
        self.addAction(
            Translator.translate("MENU_BAR_CLOSE_ACTION_NAME"),
            Translator.translate("MENU_BAR_CLOSE_ACTION_STATUS_TIP"),
            lambda: parent.tab.remove_tab(parent.tab.tabs.currentIndex),
            "close",
            file_menu,
            file_toolbar,
        )

        self.addSeparator(file_menu, self.contextMenu)

        self.addAction(
            Translator.translate("MENU_BAR_LOAD_SESSION_ACTION_NAME"),
            Translator.translate("MENU_BAR_LOAD_SESSION_ACTION_STATUS_TIP"),
            parent.load_session,
            "load_session",
            file_menu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_SAVE_SESSION_ACTION_NAME"),
            Translator.translate("MENU_BAR_SAVE_SESSION_ACTION_STATUS_TIP"),
            parent.save_session,
            "save_session",
            file_menu,
        )

        self.addSeparator(file_menu)

        self.addAction(
            Translator.translate("MENU_BAR_EXIT_ACTION_NAME"),
            Translator.translate("MENU_BAR_EXIT_ACTION_STATUS_TIP"),
            parent.close,
            "exit",
            file_menu,
        )

        edit_menu = self.addMenu(Translator.translate("MENU_BAR_EDIT_MENU"), menuBar)
        edit_toolbar = self.addToolbar(Translator.translate("MENU_BAR_EDIT_TOOLBAR"))

        self.addAction(
            Translator.translate("MENU_BAR_UNDO_ACTION_NAME"),
            Translator.translate("MENU_BAR_UNDO_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).undo(),
            "undo",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_REDO_ACTION_NAME"),
            Translator.translate("MENU_BAR_REDO_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).redo(),
            "redo",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )

        self.addSeparator(edit_menu, self.contextMenu)

        self.addAction(
            Translator.translate("MENU_BAR_CUT_ACTION_NAME"),
            Translator.translate("MENU_BAR_CUT_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).cut(),
            "cut",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_COPY_ACTION_NAME"),
            Translator.translate("MENU_BAR_COPY_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).copy(),
            "copy",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_PASTE_ACTION_NAME"),
            Translator.translate("MENU_BAR_PASTE_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).paste(),
            "paste",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_SELECT_ALL_ACTION_NAME"),
            Translator.translate("MENU_BAR_SELECT_ALL_ACTION_STATUS_TIP"),
            lambda: parent.tab.tabs.currentWidget()
            .findChild(QPlainTextEdit)
            .selectAll(),
            "redo",
            edit_menu,
            self.contextMenu,
        )

        self.addSeparator(edit_menu, self.contextMenu)

        self.addAction(
            Translator.translate("MENU_BAR_PREVIEW_ACTION_NAME"),
            Translator.translate("MENU_BAR_PREVIEW_ACTION_STATUS_TIP"),
            lambda: Previewer(parent.tab.tabs.currentWidget().data, parent),
            "preview",
            edit_menu,
            edit_toolbar,
            self.contextMenu,
        )

        element_menu = self.addMenu(
            Translator.translate("MENU_BAR_INSERT_MENU"), edit_menu, self.contextMenu
        )

        for element in skippy.utils.elements.Elements.elements:
            name = element.__alias__ if element.__alias__ else element.__name__
            self.addAction(
                name,
                name,
                partial(ElementGenerator, element, parent),
                None,
                element_menu,
            )

        settings_menu = self.addMenu(
            Translator.translate("MENU_BAR_SETTINGS_MENU"), menuBar
        )

        self.addAction(
            Translator.translate("MENU_BAR_TOGGLE_THEME_ACTION_NAME"),
            Translator.translate("MENU_BAR_TOGGLE_THEME_ACTION_STATUS_TIP"),
            parent.toggle_theme,
            "toggle",
            settings_menu,
        )

        language_menu = self.addMenu(
            Translator.translate("MENU_BAR_LANGUAGES_MENU"), settings_menu
        )

        for lang in Translator.languages():
            name = Translator.getLangName(lang)
            self.addAction(
                name, name, partial(parent.updateTranslate, lang), None, language_menu
            )

        self.addSeparator(settings_menu)

        self.addAction(
            Translator.translate("MENU_BAR_LOGIN_ACTION_NAME"),
            Translator.translate("MENU_BAR_LOGIN_ACTION_STATUS_TIP"),
            parent.login,
            "login",
            settings_menu,
        )
        self.addAction(
            Translator.translate("MENU_BAR_LOGOUT_ACTION_NAME"),
            Translator.translate("MENU_BAR_LOGOUT_ACTION_STATUS_TIP"),
            parent.logout,
            "logout",
            settings_menu,
        )

    def addMenu(self, label="", *widgets):
        menu = QMenu(label, self.parent)
        for widget in widgets:
            widget.addMenu(menu)

        return menu

    def addToolbar(self, label):
        toolbar = QToolBar(label, self.parent)
        toolbar.setIconSize(QSize(20, 20))
        self.parent.addToolBar(toolbar)

        return toolbar

    def addSeparator(self, *menus):
        for menu in menus:
            menu.addSeparator()

    def addAction(self, label, statusTip, func, img, *menus):
        action = QAction(
            label,
            self,
        )

        if img:
            action.setIcon(
                QIcon(
                    os.path.join(
                        skippy.config.ASSETS_FOLDER,
                        self.parent.settings.value("mode", "light"),
                        f"{img}.png",
                    )
                )
            )
            self.action_list[action] = img
        action.setStatusTip(statusTip)
        action.triggered.connect(func)
        for menu in menus:
            menu.addAction(action)

        return action


class LoginStatusWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginStatusWidget, self).__init__(parent)
        self.parent = parent
        self.setGeometry(300, 300, 300, 50)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("", self)
        self.label.setFont(QFont("Arial", 10))

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        username = skippy.utils.profile.Profile.load()[0]
        if username != "" and username != None:
            self.label.setText(
                Translator.translate("SIGNED_IN_AS_LABEL").format(username)
            )
        else:
            self.label.setText("")

    def set_text(self, text):
        self.label.setText(Translator.translate("SIGNED_IN_AS_LABEL").format(text))


class ProjectList(QWidget):
    def __init__(self, parent=None):
        super(ProjectList, self).__init__(parent)
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
            self.parent.session.save()

        title_box = QLineEdit()
        title_box.setText(title)
        title_box.textEdited.connect(
            lambda: self.tabs.setTabText(self.tabs.currentIndex(), title_box.text())
        )
        title_box.textEdited.connect(lambda text: setData("title", text))
        title_box.textEdited.connect(self.parent.update_title)
        title_box.setStyleSheet("QLineEdit{font-family: Arial; font-size:11pt;}")

        editor = CustomPlainTextEdit(self.parent, self)
        editor.setPlainText(source)
        editor.textChanged.connect(lambda: setData("source", editor.toPlainText()))
        editor.setStyleSheet("QPlainTextEdit{font-family: Arial; font-size:11pt;}")

        tags_box = QLineEdit()
        if isinstance(tags, collections.Iterable):
            tags_box.setText(" ".join(tags))
        tags_box.textChanged.connect(lambda text: setData("tags", text.split(" ")))
        tags_box.setStyleSheet("QLineEdit{font-family: Arial; font-size:11pt;}")

        files_button = QPushButton(Translator.translate("FILES_BUTTON"), self)
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
        self.worker.finished.connect(self.parent.session.save)
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


class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, mainWindow, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)
        self.mainWindow = mainWindow

    def contextMenuEvent(self, event):
        self.mainWindow.menus.contextMenu.exec_(self.mapToGlobal(event.pos()))


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
        super(FilesDialog, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.label = QLabel(Translator.translate("FILES_DIALOG_FILES_LIST_LABEL"), self)
        self.label.setFont(QFont("Arial", 10))

        self.fileWidget = FilesWidget(widget, self)

        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        if self.fileWidget.layout.count():
            self.layout.addWidget(self.fileWidget, alignment=Qt.AlignCenter)
        else:
            self.empty_files_label = QLabel(
                Translator.translate("FILES_DIALOG_EMPTY_FILES_LIST_LABEL"), self
            )
            self.layout.addWidget(self.empty_files_label, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(300, 300)
        self.resize(200, 100)
        self.show()


class FilesWidget(QWidget):
    def __init__(self, widget, parent=None):
        super(FilesWidget, self).__init__(parent)
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
        super(FileWidget, self).__init__(parent)
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
        super(LoginDialog, self).__init__(parent)
        self.parent = parent

        self.auth = False

        self.layout = QVBoxLayout(self)

        self.label = QLabel(
            Translator.translate("DIALOG_SIGN_IN_TO_WIKIDOT_LABEL"), self
        )
        self.login_box = QLineEdit()
        self.login_box.setPlaceholderText(
            Translator.translate("DIALOG_LOGIN_PLACEHOLDER")
        )
        self.password_box = QLineEdit()
        self.password_box.setEchoMode(QLineEdit.Password)
        self.password_box.setPlaceholderText(
            Translator.translate("DIALOG_PASSWORD_PLACEHOLDER")
        )
        self.button = QPushButton(Translator.translate("DIALOG_OK_BUTTON"), self)

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
        super(UploadDialog, self).__init__(parent)
        self.widget = widget
        self.layout = QVBoxLayout(self)

        self.sites = {}

        def addSites(sites):
            if sites[0] in self.sites:
                addSites((sites[0] + "(1)", sites[1]))
            else:
                self.sites[sites[0]] = sites[1]
                self.site_box.addItem(sites[0])

        self.label = QLabel(Translator.translate("DIALOG_ENTER_PAGE_LABEL"), self)
        self.site_box = QComboBox(self)
        self.thread = QThread()
        self.worker = GetSites()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(addSites)
        self.page_box = QLineEdit()
        self.page_box.setPlaceholderText(
            Translator.translate("DIALOG_PAGE_BOX_PLACEHOLDER")
        )
        self.comment_box = QLineEdit()
        self.comment_box.setText(Translator.translate("DIALOG_COMMENT_BOX_TEXT"))
        self.comment_box.setPlaceholderText(
            Translator.translate("DIALOG_COMMENT_BOX_PLACEHOLDER")
        )
        self.button = QPushButton(Translator.translate("DIALOG_OK_BUTTON"), self)

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
            try:
                p.upload(file, base64.b64decode(self.widget.data["files"][file]))
                log.debug(f"File {file} is uploaded")
            except RuntimeError as e:
                log.debug(f"RuntimeError({str(e)}): File {file} isn't uploaded")
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
        super(DownloadDialog, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.sites = {}

        def addSites(sites):
            if sites[0] in self.sites:
                addSites((sites[0] + "(1)", sites[1]))
            else:
                self.sites[sites[0]] = sites[1]
                self.site_box.addItem(sites[0])

        self.label = QLabel(Translator.translate("DIALOG_ENTER_PAGE_LABEL"), self)
        self.site_box = QComboBox(self)
        self.thread = QThread()
        self.worker = GetSites()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.progress.connect(addSites)
        self.page_box = QLineEdit()
        self.page_box.setPlaceholderText(
            Translator.translate("DIALOG_PAGE_BOX_PLACEHOLDER")
        )
        self.button = QPushButton(Translator.translate("DIALOG_OK_BUTTON"), self)

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
        self.parent.session.save()
        log.debug(f"""Download page from "{self.sites[site].site}" """)
        self.close()

    def closeEvent(self, e):
        self.worker.stop()
        e.accept()


class Previewer(QDialog):
    def __init__(self, data, parent=None):
        super(Previewer, self).__init__(parent)
        self.html = Preview(data).process()

        self.layout = QVBoxLayout(self)

        self.webEngineView = QWebEngineView()
        self.webEngineView.load(QUrl.fromLocalFile(self.html))

        self.layout.addWidget(self.webEngineView)

        self.setLayout(self.layout)

        self.setWindowTitle(f"skippy - {skippy.config.version}")
        self.move(parent.x(), parent.y())
        self.resize(parent.width(), parent.height())
        self.setWindowState(parent.windowState())

        self.show()


class ElementGenerator(QDialog):
    def __init__(self, element, parent=None):
        super(ElementGenerator, self).__init__(parent)
        self.element = element()
        self.parent = parent

        self.layout = QVBoxLayout(self)

        self.element_data = QLabel(
            f"{self.element.__alias__} - {self.element.__description__}", self
        )
        self.element_data.setWordWrap(True)

        self.layout.addWidget(self.element_data)
        self.layout.addWidget(QHLine())

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.fields = {}
        for field in self.element.requiredFieldList:
            label = QLabel(field.name if field.name else field.tag, self)

            line = QPlainTextEdit(self)
            line.setFixedHeight(50)
            line.setPlaceholderText(field.description)
            line.textChanged.connect(self.updatePreview)
            self.fields[field.tag] = line

            self.vbox.addWidget(label)
            self.vbox.addWidget(line)

        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.layout.addWidget(self.scroll)

        self.preview = QPlainTextEdit(self)
        self.preview.setReadOnly(True)

        self.layout.addWidget(self.preview)

        self.button = QPushButton(Translator.translate("DIALOG_GENERATE_BUTTON"), self)
        self.button.clicked.connect(self.process)
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.updatePreview()

        self.setWindowTitle(
            f"{self.element.__alias__} | skippy - {skippy.config.version}"
        )
        self.move(300, 300)
        self.resize(500, 400)

        self.show()

    @skippy.utils.critical.critical
    def updatePreview(self, *args):
        self.preview.setPlainText(self.generate)

    @skippy.utils.critical.critical
    def process(self, *args):
        self.parent.tab.tabs.currentWidget().findChild(QPlainTextEdit).insertPlainText(
            self.generate
        )
        self.close()

    @property
    def generate(self):
        data = {}
        for field in self.fields:
            data[field] = self.fields[field].toPlainText()
        return self.element.generate(**data)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class GetSites(QObject):
    progress = pyqtSignal(tuple)
    finished = pyqtSignal()
    cache = []
    run = True

    def run(self):
        sites = list(pyscp.wikidot.User(skippy.utils.profile.Profile.load()[0]).member)
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
