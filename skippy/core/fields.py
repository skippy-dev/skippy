from skippy.gui import components

from abc import ABCMeta, abstractmethod
from typing import Optional, Type, Any


class AbstractField(metaclass=ABCMeta):
    _component: Type[components.AbstractComponent]

    def __init__(self, alias: str, description: Optional[str] = None, default: Optional[Any] = None):
        self.alias = alias
        self.description = description if description else ""

        self.default = default
        self.value: Optional[Any] = None

        if self.default:
            self.value = self.default

    def __get__(self, instance, owner) -> Any:
        return self.value

    def __set__(self, instance, value: Any):
        self.value = value

    @property
    def component(self) -> components.AbstractComponent:
        return self._component(self.alias, self.description)

    @abstractmethod
    def from_toml(self, text: str):
        pass

    @abstractmethod
    def to_toml(self) -> str:
        pass


class TextField(AbstractField):
    _component = components.TextComponent

    def from_toml(self, text: str):
        self.value = text

    def to_toml(self) -> str:
        return self.value


class IntegerField(AbstractField):
    _component = components.IntegerComponent

    def from_toml(self, integer: int):
        self.value = integer

    def to_toml(self) -> int:
        return int(self.value)
