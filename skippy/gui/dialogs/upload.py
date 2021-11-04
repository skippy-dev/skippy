from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.api import PageData

from skippy.gui import sitebox, workers, thread

from skippy.utils import translator
import skippy.config

from typing import Optional
import os


class UploadDialog(QtWidgets.QDialog):
    def __init__(self, pdata: PageData, parent: Optional[QtCore.QObject] = None):
        super(UploadDialog, self).__init__(parent)
        self.pdata = pdata

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            translator.Translator().translate("DIALOG_ENTER_PAGE_LABEL"), self
        )

        self.site_box = sitebox.SiteBox(self, self.pdata["link"][0] if self.pdata["link"] else "")

        self.page_box = QtWidgets.QLineEdit()
        self.page_box.setPlaceholderText(
            translator.Translator().translate("DIALOG_PAGE_BOX_PLACEHOLDER")
        )
        self.page_box.setText(self.pdata["link"][1] if self.pdata["link"] else "")

        self.comment_box = QtWidgets.QLineEdit()
        self.comment_box.setText(
            translator.Translator().translate("DIALOG_COMMENT_BOX_TEXT")
        )
        self.comment_box.setPlaceholderText(
            translator.Translator().translate("DIALOG_COMMENT_BOX_PLACEHOLDER")
        )

        self.button = QtWidgets.QPushButton(
            translator.Translator().translate("DIALOG_OK_BUTTON"), self
        )
        self.button.clicked.connect(self.upload)

        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.site_box)
        self.layout.addWidget(self.page_box)
        self.layout.addWidget(self.comment_box)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle(f"Skippy - {skippy.config.version}")
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(skippy.config.RESOURCES_FOLDER, "skippy.ico"))
        )
        self.move(300, 300)
        self.resize(200, 100)

        self.show()

    def upload(self):
        site = self.site_box.currentText()
        page = self.page_box.text()
        comment = self.comment_box.text()

        self.pdata["link"] = [site, page]

        self._thread = thread.Thread(workers.UploadWorker(self.pdata, comment))
        self._thread.start()

        self.close()
