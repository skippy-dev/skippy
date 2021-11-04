from PyQt5 import QtWidgets, QtCore

from skippy.utils import translator, filehandlers

from typing import Optional


class LoginStatus(QtWidgets.QLabel):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(LoginStatus, self).__init__(parent)
        self.setFixedWidth(self.width() + 100)
        self.updateStatus(filehandlers.ProfileHandler().load()[0])

    def updateStatus(self, username: str):
        if username:
            self.setText(translator.Translator().translate("SIGNED_IN_AS_LABEL").format(username))
        else:
            self.setText("")