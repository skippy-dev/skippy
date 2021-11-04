from PyQt5 import QtWidgets

from skippy.api import critical

from skippy.core import autoupdate, scpclient

from skippy.gui.dialogs import login, updater
from skippy.gui.mainwindow import Skippy

from skippy.utils import filehandlers, logger

import sys


@critical
def start_ui():
    """Start Skippy application.
    """
    logger.log.info("Skippy was started...")

    scpclient.SCPClient(*filehandlers.ProfileHandler().load())
    
    exit_code = Skippy.EXIT_CODE_REBOOT
    while exit_code == Skippy.EXIT_CODE_REBOOT:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("skippy")

        window = Skippy()

        result = True
        updateClient = autoupdate.AbstractUpdateClient.getClient()
        if updateClient.checkVersion():
            result = updater.UpdaterDialog(updateClient.version, updateClient.update)

        if not filehandlers.ProfileHandler().load()[0]:
            result = login.LoginDialog().result()

        if not result:
            break

        window.show()

        exit_code = app.exec_()
        app = None
    logger.log.info("Skippy was stopped...")

    return exit_code
