from PyQt5 import QtWidgets, QtGui

import skippy.config


class CriticalMessageBox(QtWidgets.QDialog):
    def __init__(self, error: str, traceback: str):
        super(CriticalMessageBox, self).__init__()
        self._layout = QtWidgets.QVBoxLayout(self)

        self.errorMessage = QtWidgets.QPlainTextEdit(self)
        self.errorMessage.setReadOnly(True)
        self.errorMessage.setPlainText(traceback)

        self._layout.addWidget(self.errorMessage)

        self.setLayout(self._layout)

        self.setWindowTitle(f"Error: {error}")
        self.setWindowIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / "skippy.ico").as_posix()))

        self.resize(530, 390)
