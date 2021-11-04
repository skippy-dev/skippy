from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.api import InlineSyntax, BlockSyntax

from skippy.gui import actionbar, workers, thread, utils

from typing import Optional
import re


inlinePatterns = [
    InlineSyntax("[", "]", True),
    InlineSyntax("//", "//", False),
    InlineSyntax("**", "**", False),
    InlineSyntax("{{", "}}", False),
    InlineSyntax("--", "--", False),
    InlineSyntax("__", "__", False),
    InlineSyntax("^^", "^^", False),
    InlineSyntax(",,", ",,", False),
    InlineSyntax("@@", "@@", False),
    InlineSyntax("@<", ">@", False),
    InlineSyntax("##", "|text##", False),
    InlineSyntax("%%", "%%", False),
    InlineSyntax("{$", "}", False),
    InlineSyntax("%%form_data{", "}", False),
    InlineSyntax("%%form_raw{", "}", False),
    InlineSyntax("%%form_hint{", "}", False),
    InlineSyntax("%%form_label{", "}", False),
    InlineSyntax("%%content{", "}", False),
]

blockPatterns = {
    "module": BlockSyntax(
        True,
        False,
        {
            "Rate": {},
            "ListPages": {
                "pagetype": "normal|hidden|*",
                "category": ".|*",
                "tags": "-|=|==",
                "parent": "-|=|-=|.",
                "link_to": ".",
                "created_at": "=|yyyy|yyyy.mm|last n unit",
                "created_by": "=|-=",
                "rating": "n|=",
                "offset": "n",
                "range": ".|before|after|others",
                "order": "property desc",
                "limit": "n",
                "perPage": "n",
                "reverse": "yes|no",
                "separate": "yes|no",
                "prependLine": "str",
                "appendLine": "str",
                "rss": "str",
                "rssDescription": "str",
                "rssHome": "uri",
                "rssLimit": "n",
                "rssOnly": "true",
                "urlAttrPrefix": "str",
            },
            "ListUsers": {"users": "."},
            "CSS": {"show": "true|false", "disable": "true|false"},
            "Redirect": {"destination": "url"},
            "ListDrafts": {"pageType": "exists|notexists"},
            "CountPages": {
                "pagetype": "normal|hidden|*",
                "category": ".|*",
                "tags": "-|=|==",
                "parent": "-|=|-=|.",
                "link_to": ".",
                "created_at": "=|yyyy|yyyy.mm|last n unit",
                "created_by": "=|-=",
                "rating": "n|=",
                "offset": "n",
                "range": ".|before|after|others",
                "prependLine": "",
                "appendLine": "",
                "urlAttrPrefix": "",
            },
            "TagCloud": {
                "mode": "3d",
                "maxFontSize": "px|pt|em|%",
                "minFontSize": "px|pt|em|%",
                "maxColor": "RRR,GGG,BBB",
                "minColor": "RRR,GGG,BBB",
                "limit": "int",
                "target": "unix_pagename",
                "category": "category",
                "showHidden": "true|false",
                "urlAttrPrefix": "str",
                "skipCategoryFromUrl": "true|false",
                "width": "int",
                "height": "int",
            },
            "PageCalendar": {
                "category": "*|category1,category2",
                "tags": "tag1,tag2",
                "startPage": "unix_pagename",
                "targetPage": "unix_pagename",
                "urlAttrPrefix": "str",
            },
            "PageTree": {
                "root": "unix_pagename",
                "showRoot": "true|false",
                "depth": "int",
            },
            "Backlinks": {},
            "WantedPages": {},
            "OrphanedPages": {},
            "Categories": {},
            "Watchers": {"noActions": "True|false"},
            "Members": {
                "group": "members|admins|moderators",
                "showSince": "no|yes",
                "order": "userID|joined|name[Desc]",
            },
            "Join": {"button": "Join this site!", "class": "my-join-button"},
            "SendInvitations": {},
            "WhoInvited": {},
            "NewPage": {
                "category": "category",
                "template": "unix_pagename",
                "size": "int",
                "button": "create page",
                "format": "/^Reg?Exp$/",
                "tags": "tag1 tag2",
                "parent": "unix_pagename",
                "mode": "edit|save-and-refresh|save-and-go",
                "goTo": "unix_pagename",
            },
            "ThemePreviewer": {"noUi": "true|false"},
            "MailForm": {
                "to": "user1,user2",
                "button": "str",
                "format": "csv",
                "title": "Email Title",
                "successPage": "unix_pagename",
            },
            "PetitionAdmin": {},
            "SiteGrid": {"limit": "int"},
            "FeaturedSite": {},
            "Feed": {
                "src": "http://path.to/feed.xml",
                "limit": "int",
                "offset": "int",
            },
            "FrontForum": {
                "category": "12,102",
                "feed": "str",
                "feedTitle": "sitename feed",
                "limit": "int",
                "offset": "int",
                "fixRelativeLinks": "true|false",
            },
            "Comments": {
                "title": "Comments",
                "hide": "true|false",
                "hideForm": "true|false",
                "order": "reverse|forwards",
            },
            "RecentPosts": {},
            "MiniRecentThreads": {"limit": "int"},
            "MiniActiveThreads": {"limit": "int"},
            "MiniRecentPosts": {"limit": "int"},
            "RatedPages": {
                "category": "category-name",
                "order": "date-created-|rating-[desc|asc]",
                "minRating": "int",
                "maxRating": "int",
                "limit": "int",
                "comments": "True|false",
            },
            "FlickrGallery": {
                "userName": "flickr-user",
                "tags": "tag1, tag2",
                "tagMode": "all|any",
                "sort": "date-posted-|date-taken-|interestingness-[desc|asc]|relevance",
                "photosetId": "photoset-id",
                "groupId": "group-name",
                "groupUrl": "flickr-url",
                "perPage": "int (1-100)",
                "limitPages": "int",
                "size": "square|thumbnail|small|medium",
                "disableBrowsing": "true|false",
                "contentType": "photos|screenshots|other|all",
            },
            "Files": {},
            "Search": {"mini": "true", "a": "p|pf|f"},
            "SearchAll": {},
            "SearchUsers": {},
            "SiteChanges": {},
            "ManageSite": {},
            "Clone": {"source": ".|site-unix-name", "button": "str"},
        },
    ),
    "collapsible": BlockSyntax(
        True,
        False,
        {
            "": {
                "show": "str",
                "hide": "str",
                "folded": "no|yes",
                "hideLocation": "both|bottom|top",
            }
        },
    ),
    "code": BlockSyntax(
        True,
        False,
        {"": {"type": "lang"}},
    ),
    "iftags": BlockSyntax(True, False),
    "toc": BlockSyntax(False, False),
    "include": BlockSyntax(False, False),
    "user": BlockSyntax(False, False),
    "*user": BlockSyntax(False, False),
    "html": BlockSyntax(True, False),
    "gallery": BlockSyntax(
        True,
        False,
        {
            "": {
                "size": "square|thumbnail|small|medium",
                "order": "name|created_at [desc]",
                "viewer": "true|false",
            }
        },
    ),
    "div": BlockSyntax(
        True,
        False,
        {"": {"style": "css: code;", "class": "css-class"}},
    ),
    "span": BlockSyntax(
        True,
        True,
        {"": {"style": "css: code;", "class": "css-class"}},
    ),
    "footnote": BlockSyntax(True, True),
    "size": BlockSyntax(True, True),
    "table": BlockSyntax(
        True,
        False,
        {"": {"style": "css: code;", "class": "css-class"}},
    ),
    "row": BlockSyntax(
        True,
        False,
        {"": {"style": "css: code;", "class": "css-class"}},
    ),
    "cell": BlockSyntax(
        True,
        False,
        {"": {"style": "css: code;", "class": "css-class"}},
    ),
    "image": BlockSyntax(
        False,
        True,
        {
            "": {
                "link": "uri",
                "alt": "str",
                "title": "str",
                "width": "px|em|%",
                "height": "px|em|%",
                "style": "css",
                "class": "css-class",
                "size": "square|thumbnail|small|medium|large",
            },
        },
    ),
    "=": BlockSyntax(True, False),
    ">": BlockSyntax(True, False),
    "<": BlockSyntax(True, False),
    "==": BlockSyntax(True, False),
}


def splitByPosition(line: str, pos: int) -> tuple[str, str]:
    return line[:pos], line[pos:]


class Completer(QtWidgets.QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(Completer, self).__init__(parent)
        self.setCompletionMode(self.PopupCompletion)
        self.highlighted.connect(self.setSelected)

        self.setWidget(parent)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.popup().clicked.connect(lambda index: self.insertText.emit(index.data()))
        self.insertText.connect(parent.insertCompletion)

        self.popup().setStyleSheet("font-family:Arial; font-size:10pt;")

    def setSelected(self, text: str):
        self.lastSelected = text

    @property
    def selected(self) -> str:
        return self.lastSelected


class AdvancedEditor(QtWidgets.QPlainTextEdit):
    RE_BLOCK = r"\[\[([\w=><]+)(?:\s(\w+)|\s|)(?:\s(\S+)|)+\]\]"

    fileDragAndDroped = QtCore.pyqtSignal(str, bytes)

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(AdvancedEditor, self).__init__(parent)
        self.completer = Completer(self)

        self.setAcceptDrops(True)

    def insertCompletion(self, completion: str):
        extra = len(completion) - len(self.completer.completionPrefix())
        if extra:
            self.insertPlainText(completion[-extra:])

    def getLineUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(cursor.BlockUnderCursor)

        return cursor.selectedText().replace("\u2029", "")

    def keyPressEvent(self, event: QtCore.QEvent):
        if (
            self.completer
            and event.key() in utils.ENTER_KEYS
            and self.completer.popup().isVisible()
        ):
            self.completer.insertText.emit(self.completer.selected)
            self.completer.popup().hide()
            return

        curentLine = self.getLineUnderCursor()
        pos = self.textCursor().positionInBlock()

        super().keyPressEvent(event)
        self.suggestingBlockParams()
        self.closeBlocks(curentLine, pos, event)
        self.appendLists(curentLine, event)
        self.completeInlineBrackets(event)

    def openCompleterPopup(self, model: list, prefix: str):
        self.completer.setModel(QtCore.QStringListModel(model, self.completer))
        self.completer.setCompletionPrefix(prefix)

        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

        rect = self.cursorRect()
        rect.setWidth(
            popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width()
        )
        self.completer.complete(rect)

    def suggestingBlockParams(self):
        selected = self.getLineUnderCursor()

        block = re.match(self.RE_BLOCK, selected)
        if not block:
            return

        word = splitByPosition(selected, self.textCursor().positionInBlock())[0]

        blockNamePrefix = block.group(1)

        if word[-len(blockNamePrefix) :] == blockNamePrefix:
            self.openCompleterPopup(list(blockPatterns), blockNamePrefix)
            return

        blockParamNamePrefix = block.group(2)
        if blockNamePrefix in blockPatterns and "" in blockPatterns[blockNamePrefix].dataVar:
            params = blockPatterns[blockNamePrefix].dataVar[""]
            if (
                blockParamNamePrefix
                and word[-len(blockParamNamePrefix) :] == blockParamNamePrefix
            ):
                self.openCompleterPopup(
                    [f'{param}="{params[param]}"' for param in params],
                    blockParamNamePrefix,
                )
                return

            blockParamsPrefix = block.group(3)
            if (
                blockParamsPrefix
                and word[-len(blockParamsPrefix) :] == blockParamsPrefix
                and blockNamePrefix in blockPatterns
            ):
                self.openCompleterPopup(
                    [f'{param}="{params[param]}"' for param in params],
                    blockParamsPrefix,
                )
                return
        else:
            if (
                blockParamNamePrefix
                and word[-len(blockParamNamePrefix) :] == blockParamNamePrefix
                and blockNamePrefix in blockPatterns
            ):
                self.openCompleterPopup(
                    list(blockPatterns[blockNamePrefix].dataVar), blockParamNamePrefix
                )
                return

            blockParamsPrefix = block.group(3)
            if (
                blockParamsPrefix
                and word[-len(blockParamsPrefix) :] == blockParamsPrefix
                and blockNamePrefix in blockPatterns
                and blockParamNamePrefix in blockPatterns[blockNamePrefix].dataVar
            ):
                params = blockPatterns[blockNamePrefix].dataVar[blockParamNamePrefix]
                self.openCompleterPopup(
                    [f'{param}="{params[param]}"' for param in params],
                    blockParamsPrefix,
                )
                return

    def closeBlocks(self, curentLine: str, pos: int, event: QtCore.QEvent):
        left = splitByPosition(curentLine, pos)[0]

        block = re.match(self.RE_BLOCK, left)
        if block:
            for key in blockPatterns:
                pattern = blockPatterns[key]
                if block.group(1) == key and pattern.closeBlock:
                    closeBlock = f"[[/{key}]]"
                    if event.key() in utils.ENTER_KEYS and not pattern.inline:
                        self.insertPlainText("\n" + closeBlock)

                        cursor = self.textCursor()
                        cursor.movePosition(cursor.Up)
                        self.setTextCursor(cursor)
                    elif (
                        event.text()
                        and event.key() not in utils.ENTER_KEYS
                        and event.key() not in utils.DELETE_KEYS
                        and pattern.inline
                        and closeBlock not in curentLine
                    ):
                        self.insertPlainText(closeBlock)

                        cursor = self.textCursor()
                        cursor.movePosition(cursor.Left, n=len(closeBlock))
                        self.setTextCursor(cursor)

    def appendLists(self, curentLine: str, event: QtCore.QEvent):
        if (
            curentLine[:2] in ("* ", "# ")
            and curentLine[:2] != curentLine
            and event.key() in utils.ENTER_KEYS
        ):
            self.insertPlainText(curentLine[:2])

    def completeInlineBrackets(self, event: QtCore.QEvent):
        selected = self.getLineUnderCursor()

        left, right = splitByPosition(selected, self.textCursor().positionInBlock())
        for pattern in inlinePatterns:
            if (
                event.text() == pattern.opening[-1:]
                and left[-len(pattern.opening) :] == pattern.opening
                and (
                    right[: len(pattern.closing)] != pattern.closing or pattern.multiple
                )
            ):
                self.insertPlainText(pattern.closing)
                cursor = self.textCursor()
                cursor.movePosition(cursor.Left, n=len(pattern.closing))
                self.setTextCursor(cursor)

    def contextMenuEvent(self, event: QtCore.QEvent):
        actionbar.ContextMenu(self).exec_(self.mapToGlobal(event.pos()))

    def dragEnterEvent(self, event: QtCore.QEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtCore.QEvent):
        self._thread = thread.Thread(
            workers.FileWorker([url.toLocalFile() for url in event.mimeData().urls()])
        )
        self._thread.worker.progress.connect(self.fileDragAndDroped.emit)
        self._thread.start()

        dummyEvent = QtGui.QDropEvent(
            event.posF(),
            event.possibleActions(),
            QtCore.QMimeData(),
            event.mouseButtons(),
            event.keyboardModifiers(),
        )
        super(AdvancedEditor, self).dropEvent(dummyEvent)
