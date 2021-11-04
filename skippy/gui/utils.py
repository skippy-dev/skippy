from PyQt5 import QtWidgets, QtCore

from typing import Optional


ENTER_KEYS = (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter)
DELETE_KEYS = (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete)


def getApplication() -> QtWidgets.QApplication:
    return QtWidgets.QApplication.instance()


def getMainWindow() -> Optional[QtWidgets.QMainWindow]:
    app = getApplication()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QtWidgets.QMainWindow):
            return widget
    return None


def showStatusMessage(message: str):
    getMainWindow().statusBar().showMessage(message)
