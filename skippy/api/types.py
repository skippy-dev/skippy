from typing import NamedTuple, TypedDict, Callable, Tuple, Dict, List, Any


class Language(NamedTuple):
    code: str
    dictionary: Dict[str, str]


class Action(NamedTuple):
    label: str
    statusTip: str
    func: Callable[..., Any]
    img: str


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
    link: Tuple[str, str]


__all__ = ["Language", "Action", "InlineSyntax", "BlockSyntax", "PageData"]
