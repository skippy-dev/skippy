from PyQt5 import QtWidgets, QtGui

import skippy.config

import os


class CriticalMessageBox(QtWidgets.QDialog):
    def __init__(self, error: str, traceback: str):
        super(CriticalMessageBox, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.errorMessage = QtWidgets.QPlainTextEdit(self)
        self.errorMessage.setReadOnly(True)
        self.errorMessage.setPlainText(traceback)

        self.layout.addWidget(self.errorMessage)

        self.setLayout(self.layout)

        self.setWindowTitle(f"Error: {error}")
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(skippy.config.RESOURCES_FOLDER, "skippy.ico"))
        )

        self.resize(530, 390)
