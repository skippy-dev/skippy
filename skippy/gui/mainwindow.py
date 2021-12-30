"""The main window of Skippy.
"""
from PyQt5 import QtWidgets, QtGui, QtCore

from skippy.api import PageData, critical

from skippy.gui.dialogs import download, upload, login
from skippy.gui import (
    actionbar,
    tabwidget,
    loginstatus,
    workers,
    thread,
    styles,
    settings,
    utils,
)

from skippy.utils import translator, filehandlers

import skippy.config

import pathlib


class Skippy(QtWidgets.QMainWindow):

    """The main window of Skippy."""

    EXIT_CODE_REBOOT = -123

    def __init__(self):
        """Create a new main window."""
        super(Skippy, self).__init__()
        self._threads = []

        self.settings = settings.Settings()

        translator.Translator().load(self.settings.lang)

        self.menuBar = actionbar.MenuBar(self)
        self.toolBar = actionbar.ToolBar(self)
        self.setMenuBar(self.menuBar)
        self.addToolBar(self.settings.toolbarArea, self.toolBar)

        self.tab = tabwidget.ProjectList(self)
        self.tab.statsChanged.connect(self.update_rpc)
        self.tab.titleChanged.connect(self.update_title)
        self.tab.load()

        self.loginStatus = loginstatus.LoginStatus(self)

        self.setCentralWidget(self.tab)

        self.status = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status)

        self.setWindowIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / "skippy.ico").as_posix()))
        self.resize(self.settings.size)
        self.move(self.settings.pos)
        self.setWindowState(QtCore.Qt.WindowState(self.settings.state))

        self.setFont(QtGui.QFont("Arial", 10))

        if self.settings.theme == "light":
            styles.light()
        else:
            styles.dark()

    def update_title(self, title: str):
        """Update title for Skippy window."""
        self.setWindowTitle(f"{title} | Skippy - {skippy.config.version}")

    def download(self):
        """Run page download dialog."""
        download.DownloadDialog(self)

    @critical
    def upload(self, pdata: PageData):
        """Upload page at prepared URL from parent field, if don't has it run upload dialog.

        Args:
            pdata (PageData): Page data
        """
        if pdata["link"]:
            uploadPageThread = thread.Thread(workers.UploadWorker(pdata))
            uploadPageThread.finished.connect(
                lambda: self.removeThread(uploadPageThread)
            )
            self._threads.append(uploadPageThread)
            uploadPageThread.start()
        else:
            self.upload_as(pdata)

    def upload_as(self, pdata: PageData):
        """Run upload dialog.

        Args:
            pdata (PageData): Page data
        """
        upload.UploadDialog(pdata, self)

    def login(self):
        """Run login dialog."""
        login.LoginDialog()

    def logout(self):
        """Logout from account and run a login dialog."""
        filehandlers.ProfileHandler().logout()
        self.hide()
        self.login()
        self.show()

    def save_session(self):
        """Save current work session to selected file."""
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", "session.json", "JSON file (*.json)\nAll files (*.*)"
        )
        if path:
            self.tab.save(pathlib.Path(path))

    def load_session(self):
        """Load session from selected file."""
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load file", "", "JSON file (*.json)\nAll files (*.*)"
        )
        if path:
            self.tab.load(pathlib.Path(path))

    def load_files(self):
        """Load files to the current page."""
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Load files", "", "All files (*.*)"
        )
        loadFileThread = thread.Thread(workers.FileWorker(files))
        loadFileThread.finished.connect(lambda: self.removeThread(loadFileThread))
        self._threads.append(loadFileThread)
        loadFileThread.worker.progress.connect(self.tab.currentWidget().uploadFile)
        loadFileThread.start()

    def update_rpc(self, title: str, words: int, letters: int):
        for thr in self._threads:
            if type(thr.worker) == workers.DiscordRPCWorker:
                return
        updateRPCThread = thread.Thread(workers.DiscordRPCWorker(title, words, letters))
        updateRPCThread.finished.connect(lambda: self.removeThread(updateRPCThread))
        self._threads.append(updateRPCThread)
        updateRPCThread.start()

    def toggle_theme(self):
        """Toggle current theme."""
        self.settings.theme = "dark" if self.settings.theme == "light" else "light"
        self.restart()

    def update_translate(self, lang: str):
        """Update translate language.

        Args:
            lang (str): Language code
        """
        self.settings.lang = lang
        self.restart()

    @classmethod
    def restart(cls):
        """Restart window."""
        utils.getApplication().exit(cls.EXIT_CODE_REBOOT)

    def removeThread(self, thr: thread.Thread):
        if thr in self._threads:
            self._threads.remove(thr)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        """Change size of login status widget when window resized.

        Args:
            event (QtGui.QResizeEvent): Resize event
        """
        self.loginStatus.move(self.width() - 200, -5)
        if self.width() < 350:
            self.loginStatus.hide()
        else:
            self.loginStatus.show()

        event.accept()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Save window state and session when app closed.

        Args:
            event (QtGui.QCloseEvent): Close event
        """
        self.settings.size = self.size()
        self.settings.pos = self.pos()
        self.settings.state = self.windowState()
        self.settings.toolbarArea = self.toolBarArea(self.toolBar)

        self.tab.save()

        event.accept()
