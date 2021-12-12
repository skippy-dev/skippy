from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.api import Action

from skippy.core.elements import elements as elems

from skippy.gui.dialogs import previewer, elements, finder
from skippy.gui import settings, utils

from skippy.utils.translator import Translator
import skippy.config

from typing import Optional, Union
from functools import partial
import os


class ActionBarBase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme = settings.Settings().theme
        mainwindow = utils.getMainWindow()

        self.new_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.NEW_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.NEW_STATUS_TIP"),
            lambda: mainwindow.tab.newTab(),
            "new",
        )

        self.open_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.OPEN_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.OPEN_STATUS_TIP"),
            lambda: mainwindow.download(),
            "open",
        )

        self.upload_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.UPLOAD_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.UPLOAD_STATUS_TIP"),
            lambda: mainwindow.upload(mainwindow.tab.currentWidget().pdata),
            "upload",
        )

        self.upload_as_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.UPLOAD_AS_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.UPLOAD_AS_STATUS_TIP"),
            lambda: mainwindow.upload_as(mainwindow.tab.currentWidget().pdata),
            "upload_as",
        )

        self.close_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.CLOSE_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.CLOSE_STATUS_TIP"),
            lambda: mainwindow.tab.removeTab(mainwindow.tab.currentIndex()),
            "close",
        )

        self.load_files_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.LOAD_FILES_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.LOAD_FILES_STATUS_TIP"),
            lambda: mainwindow.load_files(),
            "load_files",
        )

        self.load_session_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.LOAD_SESSION_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.LOAD_SESSION_STATUS_TIP"),
            lambda: mainwindow.load_session(),
            "load_session",
        )

        self.save_session_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.SAVE_SESSION_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.SAVE_SESSION_STATUS_TIP"),
            lambda: mainwindow.save_session(),
            "save_session",
        )

        self.exit_action = Action(
            Translator().translate("MENU_BAR.ACTION.FILE.EXIT_NAME"),
            Translator().translate("MENU_BAR.ACTION.FILE.EXIT_STATUS_TIP"),
            lambda: mainwindow.close(),
            "exit",
        )

        self.undo_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.UNDO_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.UNDO_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.undo(),
            "undo",
        )

        self.redo_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.REDO_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.REDO_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.redo(),
            "redo",
        )

        self.cut_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.CUT_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.CUT_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.cut(),
            "cut",
        )

        self.copy_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.COPY_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.COPY_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.copy(),
            "copy",
        )

        self.paste_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.PASTE_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.PASTE_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.paste(),
            "paste",
        )

        self.select_all_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.SELECT_ALL_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.SELECT_ALL_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.selectAll(),
            "select_all",
        )

        self.find_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.FIND_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.FIND_STATUS_TIP"),
            lambda: finder.FinderDialog(mainwindow),
            "find",
        )

        self.preview_action = Action(
            Translator().translate("MENU_BAR.ACTION.EDIT.PREVIEW_NAME"),
            Translator().translate("MENU_BAR.ACTION.EDIT.PREVIEW_STATUS_TIP"),
            lambda: previewer.Previewer(
                mainwindow.tab.currentWidget().pdata, mainwindow
            ).deleteLater(),
            "preview",
        )

        self.toggle_theme_action = Action(
            Translator().translate("MENU_BAR.ACTION.SETTINGS.TOGGLE_THEME_NAME"),
            Translator().translate("MENU_BAR.ACTION.SETTINGS.TOGGLE_THEME_STATUS_TIP"),
            lambda: mainwindow.toggle_theme(),
            "toggle",
        )

        self.toggle_autocomplete_action = Action(
            Translator().translate("MENU_BAR.ACTION.SETTINGS.TOGGLE_AC_NAME"),
            Translator().translate("MENU_BAR.ACTION.SETTINGS.TOGGLE_AC_STATUS_TIP"),
            lambda: mainwindow.settings.setValue(
                "acEnabled",
                {"true": False, "false": True}[mainwindow.settings.acEnabled],
            ),
            "toggle",
        )

        self.elements_menu = QtWidgets.QMenu(
            Translator().translate("MENU_BAR.ACTION.EDIT.INSERT_MENU")
        )
        for elem in elems:
            element = elem()
            self.addAction(
                Action(
                    Translator().translate(element.__alias__),
                    Translator().translate(element.__description__),
                    partial(elements.ElementDialog, element, mainwindow),
                ),
                self.elements_menu,
            )

        self.login_action = Action(
            Translator().translate("MENU_BAR.ACTION.SETTINGS.LOGIN_NAME"),
            Translator().translate("MENU_BAR.ACTION.SETTINGS.LOGIN_STATUS_TIP"),
            lambda: mainwindow.login(),
            "login",
        )

        self.logout_action = Action(
            Translator().translate("MENU_BAR.ACTION.SETTINGS.LOGOUT_NAME"),
            Translator().translate("MENU_BAR.ACTION.SETTINGS.LOGOUT_STATUS_TIP"),
            lambda: mainwindow.logout(),
            "logout",
        )

        self.language_menu = QtWidgets.QMenu(
            Translator().translate("MENU_BAR.ACTION.SETTINGS.LANGUAGES_MENU")
        )
        for lang in Translator().languages():
            name = Translator().get_lang_name(lang)
            self.addAction(
                Action(name, name, partial(mainwindow.update_translate, lang)),
                self.language_menu,
            )

    def addAction(
        self, action: Action, menu: Optional[QtWidgets.QMenu] = None
    ) -> QtWidgets.QAction:
        qaction = QtWidgets.QAction(action.label, self)

        if action.img:
            qaction.setIcon(QtGui.QIcon((skippy.config.RESOURCES_FOLDER / self.theme / f"{action.img}.png").as_posix()))

        qaction.setStatusTip(action.statusTip)
        qaction.triggered.connect(action.func)

        if menu:
            menu.addAction(qaction)
        else:
            super().addAction(qaction)

        return qaction

    def addMenu(
        self, qmenu: Union[str, QtWidgets.QMenu], menu: Optional[QtWidgets.QMenu] = None
    ) -> QtWidgets.QMenu:
        if type(qmenu) == str:
            qmenu = QtWidgets.QMenu(qmenu, self)

        if menu:
            menu.addMenu(qmenu)
        else:
            super().addMenu(qmenu)

        return qmenu


class MenuBar(ActionBarBase, QtWidgets.QMenuBar):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(MenuBar, self).__init__(parent)
        self.file_menu = self.addMenu(Translator().translate("MENU_BAR.FILE_MENU"))
        self.addAction(self.new_action, self.file_menu)
        self.addAction(self.open_action, self.file_menu)
        self.addAction(self.upload_action, self.file_menu)
        self.addAction(self.upload_as_action, self.file_menu)
        self.addAction(self.close_action, self.file_menu)
        self.file_menu.addSeparator()
        self.addAction(self.load_files_action, self.file_menu)
        self.file_menu.addSeparator()
        self.addAction(self.load_session_action, self.file_menu)
        self.addAction(self.save_session_action, self.file_menu)
        self.file_menu.addSeparator()
        self.addAction(self.exit_action, self.file_menu)

        self.edit_menu = self.addMenu(Translator().translate("MENU_BAR.EDIT_MENU"))
        self.addAction(self.undo_action, self.edit_menu)
        self.addAction(self.redo_action, self.edit_menu)
        self.edit_menu.addSeparator()
        self.addAction(self.cut_action, self.edit_menu)
        self.addAction(self.copy_action, self.edit_menu)
        self.addAction(self.paste_action, self.edit_menu)
        self.addAction(self.select_all_action, self.edit_menu)
        self.edit_menu.addSeparator()
        self.addAction(self.find_action, self.edit_menu)
        self.edit_menu.addSeparator()
        self.addAction(self.preview_action, self.edit_menu)
        self.addMenu(self.elements_menu, self.edit_menu)

        self.settings_menu = self.addMenu(
            Translator().translate("MENU_BAR.SETTINGS_MENU")
        )
        self.addAction(self.toggle_theme_action, self.settings_menu)
        self.addAction(self.toggle_autocomplete_action, self.settings_menu)
        self.settings_menu.addMenu(self.language_menu)
        self.settings_menu.addSeparator()
        self.addAction(self.login_action, self.settings_menu)
        self.addAction(self.logout_action, self.settings_menu)


class ToolBar(ActionBarBase, QtWidgets.QToolBar):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(ToolBar, self).__init__(parent)
        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.upload_action)
        self.addAction(self.upload_as_action)
        self.addAction(self.close_action)
        self.addAction(self.load_files_action)
        self.addAction(self.undo_action)
        self.addAction(self.redo_action)
        self.addAction(self.cut_action)
        self.addAction(self.copy_action)
        self.addAction(self.paste_action)
        self.addAction(self.select_all_action)
        self.addAction(self.preview_action)

        self.setAllowedAreas(QtCore.Qt.LeftToolBarArea | QtCore.Qt.TopToolBarArea)


class ContextMenu(ActionBarBase, QtWidgets.QMenu):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(ContextMenu, self).__init__(parent)
        self.addAction(self.new_action)
        self.addAction(self.load_files_action)
        self.addSeparator()
        self.addAction(self.undo_action)
        self.addAction(self.redo_action)
        self.addSeparator()
        self.addAction(self.cut_action)
        self.addAction(self.copy_action)
        self.addAction(self.paste_action)
        self.addAction(self.select_all_action)
        self.addSeparator()
        self.addAction(self.preview_action)
        self.addMenu(self.elements_menu)
