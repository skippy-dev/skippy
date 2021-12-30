from PyQt5 import QtWidgets, QtCore, QtGui

from typing import Optional, Any


class AbstractComponent(QtWidgets.QWidget):
    @property
    def valueChanged(self):
        raise NotImplementedError

    def __init__(self, alias: str, description: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.alias = alias
        self.description = description

    @property
    def value(self) -> Any:
        raise NotImplementedError

    @value.setter
    def value(self, value: Any):
        raise NotImplementedError


class TextComponent(QtWidgets.QLineEdit, AbstractComponent):
    valueChanged = QtCore.pyqtSignal()

    def __init__(self, alias: str, description: str, parent: Optional[QtWidgets.QWidget] = None):
        super(TextComponent, self).__init__(alias, description, parent)
        self.setPlaceholderText(self.description)

        self.textChanged.connect(self.valueChanged.emit)

    @property
    def value(self) -> str:
        return self.text()

    @value.setter
    def value(self, value: str):
        self.valueChanged.emit()
        self.setText(value)


class IntegerComponent(TextComponent):
    def __init__(self, alias: str, description: str, parent: Optional[QtWidgets.QWidget] = None):
        super(IntegerComponent, self).__init__(alias, description, parent)
        self.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("(?:-|)\d+"), self))

    @property
    def value(self) -> int:
        value = self.text()
        if value and value != "-":
            return int(value)
        return 0

    @value.setter
    def value(self, value: int):
        self.valueChanged.emit()
        self.setText(str(value))
