from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.api import PageData

from skippy.core import preview

from skippy.gui import thread, utils

from skippy.utils import translator

import skippy.config

from typing import Optional
import tempfile

try:
    from PyQt5 import QtWebEngineWidgets

    class PreviewerWorker(thread.AbstractWorker):
        finished = QtCore.pyqtSignal(str)

        def __init__(self, pdata: PageData):
            super(PreviewerWorker, self).__init__()
            self.pdata = pdata

        def run(self):
            self.finished.emit(preview.render(self.pdata))


    class Previewer(QtWidgets.QDialog):
        def __init__(self, pdata: PageData, parent: Optional[QtWidgets.QWidget] = None):
            super(Previewer, self).__init__(parent)
            self._layout = QtWidgets.QVBoxLayout(self)

            self.webEngineView = QtWebEngineWidgets.QWebEngineView(self)

            self._thread = thread.Thread(PreviewerWorker(pdata))
            self._thread.worker.finished.connect(self.load)
            self._thread.start()

            self._layout.addWidget(self.webEngineView)

            self.setLayout(self._layout)

            self.setWindowTitle(f"Skippy - {skippy.config.version}")
            self.setWindowIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / "skippy.ico").as_posix()))

            mainwindow = utils.getMainWindow()

            self.move(mainwindow.x(), mainwindow.y())
            self.resize(mainwindow.width(), mainwindow.height())
            self.setWindowState(mainwindow.windowState())

            self.exec_()

        def load(self, html: str):
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".html", mode="w", encoding="utf-8"
            ) as tmp:
                tmp.write(html)
                self.webEngineView.load(QtCore.QUrl.fromLocalFile(tmp.name))
except ImportError:
    class Previewer(QtWidgets.QMessageBox):
        def __init__(self, _: PageData, parent: Optional[QtWidgets.QWidget] = None):
            super(Previewer, self).__init__(parent)
            self.setText(translator.Translator().translate("DIALOG.DONT_HAVE_QTWEBENGINE_LABEL"))

            self.addButton(QtWidgets.QMessageBox.Ok)

            self.setWindowTitle(f"Skippy - {skippy.config.version}")
            self.setWindowIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / "skippy.ico").as_posix()))

            self.exec_()
