from skippy.gui import components

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any


class AbstractSetting(metaclass=ABCMeta):
    __alias__: str
    __description__: str

    _component: components.AbstractComponent

    def __init__(self):
        self.component = self._component()

    @abstractproperty
    def value(self) -> Any:
        pass

    @value.setter
    def value(self, value: Any):
        pass

    @abstractmethod
    def from_toml(self, text: str):
        pass

    @abstractmethod
    def to_toml(self) -> str:
        pass
