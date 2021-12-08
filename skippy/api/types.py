from typing import (
    MutableMapping,
    NamedTuple,
    TypedDict,
    Callable,
    Optional,
    Tuple,
    Dict,
    List,
    Any,
)


class Language(NamedTuple):
    code: str
    dictionary: MutableMapping[str, Any]


class Field(NamedTuple):
    tag: str
    name: str
    description: str


class Action(NamedTuple):
    label: str
    statusTip: str
    func: Callable[..., Any]
    img: Optional[str] = None


class InlineSyntax(NamedTuple):
    opening: str
    closing: str
    multiple: bool


class BlockSyntax(NamedTuple):
    closeBlock: bool
    inline: bool
    dataVar: Dict[str, Dict[str, str]] = {"": {}}


class PageData(TypedDict):
    title: str
    source: str
    tags: List[str]
    files: Dict[str, str]
    link: Optional[Tuple[str, str]]


__all__ = ["Language", "Field", "Action", "InlineSyntax", "BlockSyntax", "PageData"]
