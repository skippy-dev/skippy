from PyQt5 import QtWidgets, QtCore

from skippy.core.elements import AbstractElement

from skippy.gui.utils import getMainWindow

from skippy.utils.translator import Translator

import skippy.config

from typing import Optional


class ElementDialog(QtWidgets.QDialog):
    def __init__(
        self, element: AbstractElement, parent: Optional[QtWidgets.QWidget] = None
    ):
        super(ElementDialog, self).__init__(parent)
        self.element = element

        self._layout = QtWidgets.QVBoxLayout(self)

        self.element_data = QtWidgets.QLabel(
            Translator().translate(self.element.__alias__)
            + " - "
            + Translator().translate(self.element.__description__),
            self,
        )
        self.element_data.setWordWrap(True)

        self._layout.addWidget(self.element_data)
        self._layout.addWidget(QHLine())

        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.fields = {}
        for field in self.element.required_fields:
            label = QtWidgets.QLabel(
                Translator().translate(field.name) if field.name else field.tag, self
            )

            line = QtWidgets.QPlainTextEdit(self)
            line.setFixedHeight(25)
            line.setPlaceholderText(Translator().translate(field.description))
            line.textChanged.connect(self.updatePreview)
            self.fields[field.tag] = line

            self.vbox.addWidget(label)
            self.vbox.addWidget(line)

        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self._layout.addWidget(self.scroll)

        self.previewer = QtWidgets.QPlainTextEdit(self)
        self.previewer.setReadOnly(True)

        self._layout.addWidget(self.previewer)

        self.button = QtWidgets.QPushButton(
            Translator().translate("DIALOG.GENERATE_BUTTON"), self
        )
        self.button.clicked.connect(self.process)
        self._layout.addWidget(self.button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(self._layout)

        self.setWindowTitle(
            f"{Translator().translate(self.element.__alias__)} | skippy - {skippy.config.version}"
        )
        self.move(300, 300)
        self.resize(500, 400)

        self.updatePreview()

        self.show()

    def updatePreview(self):
        self.previewer.setPlainText(self.preview())

    def process(self):
        getMainWindow().tab.currentWidget().editor.insertPlainText(self.preview())
        self.close()

    def preview(self):
        return self.element.preview(
            {field: self.fields[field].toPlainText() for field in self.fields}
        )


class QHLine(QtWidgets.QFrame):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(QHLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
