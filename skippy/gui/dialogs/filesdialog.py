from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.gui import utils

from skippy.utils import translator

import skippy.config

from typing import Optional, Dict
import os


class FilesDialog(QtWidgets.QDialog):
    def __init__(self, files: Dict[str, str], parent: Optional[QtCore.QObject] = None):
        super(FilesDialog, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            translator.Translator().translate("FILES_DIALOG_FILES_LIST_LABEL"), self
        )
        self.label.setFont(QtGui.QFont("Arial", 10))

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)

        self.fileWidget = FilesWidget(files, self)
        self.fileWidget.filesListUpdated.connect(self.update)
        self.scrollArea.setWidget(self.fileWidget)

        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.scrollArea, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

        self.move(300, 300)
        self.resize(300, 200)
        self.setWindowTitle(f"Skippy - {skippy.config.version}")

        self.show()


class FilesWidget(QtWidgets.QWidget):
    filesListUpdated = QtCore.pyqtSignal()

    def __init__(self, files: Dict[str, str], parent: Optional[QtCore.QObject] = None):
        super(FilesWidget, self).__init__(parent)
        self.files = files
        self.layout = QtWidgets.QVBoxLayout(self)

        self.fileWidgets = {}
        for title in self.files:
            fileWidget = FileLineEdit(title, self)
            fileWidget.fileNameChanged.connect(self.updateFileName)
            fileWidget.fileRemoved.connect(self.removeFile)
            self.layout.addWidget(fileWidget)
            self.fileWidgets[title] = fileWidget

        self.setLayout(self.layout)

    def updateFileName(self, old: str, new: str):
        self.files[new] = self.files.pop(old)

    def removeFile(self, file: str):
        del self.files[file]
        self.fileWidgets[file].setParent(None)

        self.resize(self.sizeHint())


class FileLineEdit(QtWidgets.QLineEdit):
    fileNameChanged = QtCore.pyqtSignal(str, str)
    fileRemoved = QtCore.pyqtSignal(str)

    def __init__(self, title: str, parent: Optional[QtCore.QObject] = None):
        super(FileLineEdit, self).__init__(title, parent)
        theme = utils.getMainWindow().settings.theme

        self._prevText = title

        self.button = QtWidgets.QToolButton(self)
        self.button.setIcon(
            QtGui.QIcon(
                os.path.join(skippy.config.RESOURCES_FOLDER, theme, "close.png")
            )
        )
        self.button.setStyleSheet("padding: 0px;")
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(lambda: self.fileRemoved.emit(self.text()))

        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.textEdited.connect(self.textEditedEvent)

        self.setStyleSheet(
            "QLineEdit {padding-right: "
            + str(buttonSize.width() + frameWidth + 1)
            + "px; }"
        )
        self.setFixedSize(200, 40)

    def textEditedEvent(self, new_text: str):
        self.fileNameChanged.emit(self._prevText, new_text)
        self._prevText = new_text

    def resizeEvent(self, event: QtCore.QEvent):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - frameWidth - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )
        super(FileLineEdit, self).resizeEvent(event)
