from PyQt5 import QtWidgets, QtCore

from skippy.core.plugins import AbstractPlugin

from skippy.utils.translator import Translator

import skippy.config

from typing import Optional


class PluginDialog(QtWidgets.QDialog):
    def __init__(self, plugin: AbstractPlugin, parent: Optional[QtWidgets.QWidget] = None):
        super(PluginDialog, self).__init__(parent)
        self.plugin = plugin

        self._layout = QtWidgets.QVBoxLayout(self)

        self.pluginDataLabel = QtWidgets.QLabel(f"<b>{self.plugin.__alias__}</b> - {self.plugin.__description__}", self)
        self.pluginDataLabel.setWordWrap(True)

        self.authorLabel = QtWidgets.QLabel(f"<b>{Translator().translate('DIALOG.PLUGINS.AUTHOR')}</b>: {self.plugin.__author__}", self)
        self.versionLabel = QtWidgets.QLabel(f"<b>{Translator().translate('DIALOG.PLUGINS.VERSION')}</b>: {self.plugin.__version__}", self)

        self._layout.addWidget(self.pluginDataLabel)
        self._layout.addWidget(self.authorLabel)
        self._layout.addWidget(self.versionLabel)
        self._layout.addWidget(QHLine(self))

        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.fields = {}
        for setting in self.plugin._fields.items():
            label = QtWidgets.QLabel(setting[1].alias, self)

            component = setting[1].component
            if setting[1].value:
                component.value = setting[1].value
            component.valueChanged.connect(self.updateSettings)
            self.fields[setting[0]] = component

            self.vbox.addWidget(label)
            self.vbox.addWidget(component)

        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self._layout.addWidget(self.scroll)

        self.setLayout(self._layout)

        self.setWindowTitle(
            f"{self.plugin.__alias__} | skippy - {skippy.config.version}"
        )
        self.move(300, 300)
        self.resize(400, 300)

        self.setStyleSheet(
            "QLabel, QLineEdit, QPlainTextEdit {font-family: Arial; font-size:10pt;}"
        )

        self.show()

    def updateSettings(self):
        for key, field in self.fields.items():
            self.plugin._fields[key].value = field.value
        self.plugin.save_settings()


class QHLine(QtWidgets.QFrame):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(QHLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
