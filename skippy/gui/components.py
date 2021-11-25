from abc import ABCMeta, abstractproperty
from typing import Any


class AbstractComponent(metaclass=ABCMeta):
    @abstractproperty
    def value(self) -> Any:
        pass

    @value.setter
    def value(self, value: Any):
        pass
