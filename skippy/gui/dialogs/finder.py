from PyQt5 import QtWidgets, QtGui

from skippy.gui.utils import getMainWindow

from skippy.utils import translator

import skippy.config

from typing import Optional
import re
import os


class FinderDialog(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(FinderDialog, self).__init__(parent)
        self.textEditor = getMainWindow().tab.currentWidget().editor

        self.lastStart = 0

        findButton = QtWidgets.QPushButton(translator.Translator().translate("DIALOG.FINDER_FIND_BUTTON"), self)
        findButton.clicked.connect(self.find)

        replaceButton = QtWidgets.QPushButton(translator.Translator().translate("DIALOG.FINDER_REPLACE_BUTTON"), self)
        replaceButton.clicked.connect(self.replace)

        allButton = QtWidgets.QPushButton(translator.Translator().translate("DIALOG.FINDER_REPLACE_ALL_BUTTON"), self)
        allButton.clicked.connect(self.replaceAll)

        self.normalRadio = QtWidgets.QRadioButton(translator.Translator().translate("FINDER_NORMAL_MODE"), self)

        regexRadio = QtWidgets.QRadioButton(translator.Translator().translate("FINDER_REGEX_MODE"), self)

        self.findField = QtWidgets.QTextEdit(self)
        self.findField.resize(250, 50)

        self.replaceField = QtWidgets.QTextEdit(self)
        self.replaceField.resize(250, 50)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.findField, 1, 0, 1, 4)
        layout.addWidget(self.normalRadio, 2, 2)
        layout.addWidget(regexRadio, 2, 3)
        layout.addWidget(findButton, 2, 0, 1, 2)

        layout.addWidget(self.replaceField, 3, 0, 1, 4)
        layout.addWidget(replaceButton, 4, 0, 1, 2)
        layout.addWidget(allButton, 4, 2, 1, 2)

        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle(f"Skippy - {skippy.config.version}")
        self.setWindowIcon(QtGui.QIcon(os.path.join(skippy.config.RESOURCES_FOLDER, "skippy.ico")))
        self.setLayout(layout)

        self.normalRadio.setChecked(True)
        self.show()

    def find(self):
        text = self.textEditor.toPlainText()
        query = self.findField.toPlainText()

        if self.normalRadio.isChecked():
            self.lastStart = text.find(query, self.lastStart+1)

            if self.lastStart >= 0:
                end = self.lastStart + len(query)
                self.moveCursor(self.lastStart, end)
            else:
                self.lastStart = 0
        else:
            pattern = re.compile(query)

            match = pattern.search(text, self.lastStart + 1)
            if match:
                self.lastStart = match.start()
                self.moveCursor(self.lastStart, match.end())
            else:
                self.lastStart = 0

    def replace(self):
        self.find()
        cursor = self.textEditor.textCursor()

        if cursor.hasSelection():
            cursor.insertText(self.replaceField.toPlainText())
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
            self.textEditor.setTextCursor(cursor)

    def replaceAll(self):
        self.lastStart = 0
        self.replace()

        while self.lastStart:
            self.replace()

    def moveCursor(self, start, end):
        cursor = self.textEditor.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, end-start)

        self.textEditor.setTextCursor(cursor)
