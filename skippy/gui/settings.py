from PyQt5 import QtCore

from typing import Any


class Settings(QtCore.QSettings):
    values = {
        "theme": "light",
        "lang": "en",
        "size": QtCore.QSize(700, 700),
        "pos": QtCore.QPoint(200, 200),
        "state": QtCore.Qt.WindowNoState,
        "toolbarArea": QtCore.Qt.LeftToolBarArea,
        "acEnabled": "true",
    }

    def __init__(self):
        super(Settings, self).__init__("skippy", "skippy")
        for key in self.allKeys():
            if key not in self.values:
                self.remove(key)

    def __getattr__(self, name: str) -> Any:
        if name in self.values:
            return self.value(name, self.values[name])
        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute {name}"
        )

    def __setattr__(self, name: str, value: Any):
        self.setValue(name, value)
