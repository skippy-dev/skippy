from PyQt5 import QtWidgets, QtCore

from skippy.api import ignore

from skippy.gui import thread

from skippy.utils import cached_property, translator, filehandlers

from requests.exceptions import RequestException
from typing import Optional, Callable, List, Any
from urllib.parse import urlparse
import pyscp


class UserSitesWorker(thread.AbstractWorker):
    finished = QtCore.pyqtSignal(list)

    def run(self):
        self.finished.emit(self.sites)

    @cached_property
    @ignore(RequestException, [])
    def sites(self) -> List[str]:
        return [
            urlparse(wiki.site).netloc
            for wiki in pyscp.wikidot.User(
                filehandlers.ProfileHandler().load()[0]
            ).member
        ]


class SiteBox(QtWidgets.QComboBox):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, default: str = ""):
        super(SiteBox, self).__init__(parent)
        self.default = default

        self._lineEdit = QtWidgets.QLineEdit(self)
        self._lineEdit.setPlaceholderText(
            translator.Translator().translate("DIALOG.SITE_BOX_LINEEDIT")
        )

        self.setLineEdit(self._lineEdit)
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
            self._lineEdit.clear()
