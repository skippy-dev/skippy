from PyQt5 import QtWidgets, QtGui

from skippy.utils import translator

import skippy.config

from typing import Callable
import os


def UpdaterDialog(version: str, update_func: Callable[[], None]):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(translator.Translator().translate("DIALOG.NEW_VERSION_AVAILABLE_LABEL").format(version))
    msgBox.setInformativeText(
        translator.Translator().translate("DIALOG.YOU_CAN_DOWNLOAD_IT_LABEL")
    )

    msgBox.addButton(
        translator.Translator().translate("DIALOG.CANCEL_BUTTON"),
        QtWidgets.QMessageBox.RejectRole,
    )
    installButton = msgBox.addButton(
        translator.Translator().translate("DIALOG.INSTALL_BUTTON"),
        QtWidgets.QMessageBox.ActionRole,
    )

    msgBox.setWindowTitle(f"Skippy - {skippy.config.version}")
    msgBox.setWindowIcon(QtGui.QIcon(os.path.join(skippy.config.RESOURCES_FOLDER, "skippy.ico")))

    msgBox.exec_()

    if msgBox.clickedButton() == installButton:
        update_func()
        return False
    return True
