from PyQt5 import QtWidgets, QtCore

from skippy.api import ConnectionErrors, ignore

from skippy.gui import thread

from skippy.utils import translator, filehandlers

from typing import Optional, List
from urllib.parse import urlparse
import functools
import pyscp


class UserSitesWorker(thread.AbstractWorker):
    finished = QtCore.pyqtSignal(list)

    def run(self):
        self.finished.emit(self.sites)

    @functools.cached_property
    @ignore(ConnectionErrors, [])
    def sites(self) -> List[str]:
        return [
            urlparse(wiki.site).netloc
            for wiki in pyscp.wikidot.User(filehandlers.ProfileHandler().load()[0]).member
        ]


class SiteBox(QtWidgets.QComboBox):
    def __init__(self, parent: Optional[QtCore.QObject] = None, default: str = ""):
        super(SiteBox, self).__init__(parent)
        self.default = default

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setPlaceholderText(
            translator.Translator().translate("SITE_BOX_LINEEDIT")
        )

        self.setLineEdit(self.lineEdit)
        self.setEditable(True)

        self.setCurrentText(default)

        self._thread = thread.Thread(UserSitesWorker())
        self._thread.worker.finished.connect(self.addSites)
        self._thread.start()

    def addSites(self, sites: List[str]):
        self.addItems(sites)
        self.setCurrentText(self.default)
        self.setCompleter(QtWidgets.QCompleter(sites))
        if not self.currentText():
            self.lineEdit.clear()
