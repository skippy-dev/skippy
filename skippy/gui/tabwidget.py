from PyQt5 import QtWidgets, QtCore

from skippy.api import PageData, ignore

from skippy.gui import settings, resources, editor, utils
from skippy.gui.dialogs import filesdialog

from skippy.utils import translator, filehandlers

from typing import Optional, List, Dict, Tuple, Any
import base64


class ProjectList(QtWidgets.QTabWidget):
    titleChanged = QtCore.pyqtSignal(str)
    statsChanged = QtCore.pyqtSignal(str, int, int)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(ProjectList, self).__init__(parent)
        resources.qInitResources()

        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(
            lambda: self.titleChanged.emit(self.currentTabText())
        )
        self.currentChanged.connect(
            lambda: self.currentWidget().statusBarStats()
            if self.currentWidget()
            else None
        )
        self.titleChanged.connect(
            lambda title: self.statsChanged.emit(title, *self.currentEditorStats())
        )

        self.setStyleSheet(
            "QTabBar{font-family: Arial; font-size:10pt;} QTabBar::close-button {image: url(:"
            + settings.Settings().theme
            + "/close.png);}"
        )
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)

    def newTab(
        self,
        title: str = "New tab",
        source: str = "",
        tags: List[str] = [],
        files: Dict[str, str] = {},
        link: Optional[Tuple[str, str]] = None,
    ):
        tab = TabWidget(title, source, tags, files, link, self)
        tab.titleChanged.connect(self.setTitle)
        tab.titleChanged.connect(self.titleChanged.emit)
        tab.sourceChanged.connect(self.save)
        tab.sourceChanged.connect(
            lambda: self.statsChanged.emit(
                self.currentTabText(), *self.currentEditorStats()
            )
        )

        self.addTab(tab, title)
        self.setCurrentIndex(self.count() - 1)

        self.save()

    def currentTabText(self) -> str:
        return self.tabText(self.currentIndex())

    @ignore(AttributeError, (0, 0))
    def currentEditorStats(self) -> Tuple[int, int]:
        return self.currentWidget().editorStats()

    def setTitle(self, text: str):
        self.setTabText(self.currentIndex(), text)

    def removeTab(self, index: int):
        super().removeTab(index)
        self.checkCount()

    def checkCount(self):
        if not self.count():
            self.newTab()

    def save(self, path: Optional[str] = None):
        session = {"session": []}
        for i in range(self.count()):
            widget = self.widget(i)
            if type(widget.pdata["tags"]) == str:
                widget.pdata["tags"] = widget.pdata["tags"].split()
            session["session"].append(widget.pdata)
        session["pos"] = self.currentIndex()

        filehandlers.SessionHandler(path).save(session)

    def load(self, path: Optional[str] = None):
        session = filehandlers.SessionHandler(path).load()

        self.clear()
        for page in session["session"]:
            self.newTab(
                page["title"],
                page["source"],
                page["tags"],
                page["files"],
                page["link"] if "link" in page else page["parent"],
            )
        self.checkCount()
        self.setCurrentIndex(session["pos"] if "pos" in session else self.count() - 1)

        self.titleChanged.emit(self.currentTabText())

        self.save()


class TabWidget(QtWidgets.QWidget):
    titleChanged = QtCore.pyqtSignal(str)
    sourceChanged = QtCore.pyqtSignal()

    def __init__(
        self,
        title: str,
        source: str,
        tags: List[str],
        files: Dict[str, str],
        link: Optional[Tuple[str, str]],
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super(TabWidget, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)

        self.pdata: PageData = {
            "title": title,
            "source": source,
            "tags": tags,
            "files": files,
            "link": link,
        }

        self.title_box = QtWidgets.QLineEdit()
        self.title_box.setText(title)
        self.title_box.textEdited.connect(self.titleChanged.emit)
        self.title_box.textEdited.connect(lambda text: self.setData("title", text))

        self.editor = editor.AdvancedEditor(self)
        self.editor.setPlainText(source)
        self.editor.textChanged.connect(self.statusBarStats)
        self.editor.textChanged.connect(
            lambda: self.setData("source", self.editor.toPlainText())
        )
        self.editor.fileDragAndDroped.connect(self.uploadFile)

        self.tags_box = QtWidgets.QLineEdit()
        self.tags_box.setText(" ".join(tags))
        self.tags_box.textChanged.connect(
            lambda text: self.setData("tags", text.split())
        )

        self.files_button = QtWidgets.QPushButton(
            translator.Translator().translate("FILES_BUTTON"), self
        )
        self.files_button.clicked.connect(
            lambda: filesdialog.FilesDialog(self.pdata["files"], self)
        )

        self._layout.addWidget(self.title_box)
        self._layout.addWidget(self.editor)
        self._layout.addWidget(self.tags_box)
        self._layout.addWidget(self.files_button)
        self.setLayout(self._layout)

        self.setStyleSheet(
            "QLineEdit, QPlainTextEdit {font-family: Arial; font-size:12pt;}"
        )

    def editorStats(self) -> Tuple[int, int]:
        content = self.editor.toPlainText()
        return len(content.split()), len(content)

    def setData(self, param: str, data: Any):
        self.pdata[param] = data
        self.sourceChanged.emit()

    def uploadFile(self, filename: str, source: bytes):
        self.pdata["files"][filename] = base64.b64encode(source).decode("utf-8")

    @ignore(AttributeError)
    def statusBarStats(self):
        words, letters = self.editorStats()
        utils.showStatusMessage(f"Words: {str(words)}, Letters: {str(letters)}")
