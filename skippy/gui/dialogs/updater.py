from PyQt5 import QtWidgets, QtGui

from skippy.utils import translator

import skippy.config

from typing import Callable


class UpdaterDialog(QtWidgets.QMessageBox):
    def __init__(self, version: str):
        super(UpdaterDialog, self).__init__()
        self.setText(
            translator.Translator()
                .translate("DIALOG.NEW_VERSION_AVAILABLE_LABEL")
                .format(version)
        )
        self.setInformativeText(
            translator.Translator().translate("DIALOG.YOU_CAN_DOWNLOAD_IT_LABEL")
        )

        self.addButton(
            translator.Translator().translate("DIALOG.CANCEL_BUTTON"),
            QtWidgets.QMessageBox.RejectRole,
        )
        self.installButton = self.addButton(
            translator.Translator().translate("DIALOG.INSTALL_BUTTON"),
            QtWidgets.QMessageBox.ActionRole,
        )

        self.setWindowTitle(f"Skippy - {skippy.config.version}")
        self.setWindowIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / "skippy.ico").as_posix()))


def show(version: str, update_func: Callable[[], None]):
    msgBox = UpdaterDialog(version)
    msgBox.exec_()

    if msgBox.clickedButton() == msgBox.installButton:
        update_func()
        return False
    return True
