from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.core.scpclient import SCPClient

from skippy.gui import utils

from skippy.utils import filehandlers, translator
import skippy.config

from typing import Optional
import os


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(LoginDialog, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            translator.Translator().translate("DIALOG_SIGN_IN_TO_WIKIDOT_LABEL"), self
        )
        self.login_box = QtWidgets.QLineEdit()
        self.login_box.setPlaceholderText(
            translator.Translator().translate("DIALOG_LOGIN_PLACEHOLDER")
        )
        self.password_box = QtWidgets.QLineEdit()
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_box.setPlaceholderText(
            translator.Translator().translate("DIALOG_PASSWORD_PLACEHOLDER")
        )
        self.button = QtWidgets.QPushButton(
            translator.Translator().translate("DIALOG_OK_BUTTON"), self
        )

        self.button.clicked.connect(self.login)

        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.login_box)
        self.layout.addWidget(self.password_box)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle(f"Skippy - {skippy.config.version}")
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(skippy.config.RESOURCES_FOLDER, "skippy.ico"))
        )
        self.move(300, 300)
        self.resize(200, 100)
        
        self.exec_()

    def login(self):
        login = self.login_box.text()
        password = self.password_box.text()

        SCPClient().auth(login, password)
        filehandlers.ProfileHandler().save(login, password)

        utils.getMainWindow().loginStatus.updateStatus(login)

        self.accept()
