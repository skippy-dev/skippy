from PyQt5 import QtWidgets, QtCore, QtGui

from skippy.api import Action

from skippy.gui.dialogs import previewer
from skippy.gui import settings, utils

from skippy.utils import translator
import skippy.config

from typing import Optional, Union
from functools import partial
import os


class ActionBarBase:
    def initActions(self):
        self.theme = settings.Settings().theme
        mainwindow = utils.getMainWindow()

        self.new_action = Action(
            translator.Translator().translate("MENU_BAR_NEW_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_NEW_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.newTab(),
            "new",
        )

        self.open_action = Action(
            translator.Translator().translate("MENU_BAR_OPEN_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_OPEN_ACTION_STATUS_TIP"),
            lambda: mainwindow.download(),
            "open",
        )

        self.upload_action = Action(
            translator.Translator().translate("MENU_BAR_UPLOAD_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_UPLOAD_ACTION_STATUS_TIP"),
            lambda: mainwindow.upload(mainwindow.tab.currentWidget().pdata),
            "upload",
        )

        self.upload_as_action = Action(
            translator.Translator().translate("MENU_BAR_UPLOAD_AS_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_UPLOAD_AS_ACTION_STATUS_TIP"),
            lambda: mainwindow.upload_as(mainwindow.tab.currentWidget().pdata),
            "upload_as",
        )

        self.close_action = Action(
            translator.Translator().translate("MENU_BAR_CLOSE_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_CLOSE_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.remove_tab(mainwindow.tab.currentIndex()),
            "close",
        )

        self.load_files_action = Action(
            translator.Translator().translate("MENU_BAR_LOAD_FILES_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_LOAD_FILES_ACTION_STATUS_TIP"),
            lambda: mainwindow.load_files(),
            "load_files",
        )

        self.load_session_action = Action(
            translator.Translator().translate("MENU_BAR_LOAD_SESSION_ACTION_NAME"),
            translator.Translator().translate(
                "MENU_BAR_LOAD_SESSION_ACTION_STATUS_TIP"
            ),
            lambda: mainwindow.load_session(),
            "load_session",
        )

        self.save_session_action = Action(
            translator.Translator().translate("MENU_BAR_SAVE_SESSION_ACTION_NAME"),
            translator.Translator().translate(
                "MENU_BAR_SAVE_SESSION_ACTION_STATUS_TIP"
            ),
            lambda: mainwindow.save_session(),
            "save_session",
        )

        self.exit_action = Action(
            translator.Translator().translate("MENU_BAR_EXIT_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_EXIT_ACTION_STATUS_TIP"),
            lambda: mainwindow.close(),
            "exit",
        )

        self.undo_action = Action(
            translator.Translator().translate("MENU_BAR_UNDO_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_UNDO_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.undo(),
            "undo",
        )

        self.redo_action = Action(
            translator.Translator().translate("MENU_BAR_REDO_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_REDO_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.redo(),
            "redo",
        )

        self.cut_action = Action(
            translator.Translator().translate("MENU_BAR_CUT_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_CUT_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.cut(),
            "cut",
        )

        self.copy_action = Action(
            translator.Translator().translate("MENU_BAR_COPY_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_COPY_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.copy(),
            "copy",
        )

        self.paste_action = Action(
            translator.Translator().translate("MENU_BAR_PASTE_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_PASTE_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.paste(),
            "paste",
        )

        self.select_all_action = Action(
            translator.Translator().translate("MENU_BAR_SELECT_ALL_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_SELECT_ALL_ACTION_STATUS_TIP"),
            lambda: mainwindow.tab.currentWidget().editor.selectAll(),
            "select_all",
        )

        self.preview_action = Action(
            translator.Translator().translate("MENU_BAR_PREVIEW_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_PREVIEW_ACTION_STATUS_TIP"),
            lambda: previewer.Previewer(mainwindow.tab.currentWidget().pdata, self),
            "preview",
        )

        self.toggle_theme_action = Action(
            translator.Translator().translate("MENU_BAR_TOGGLE_THEME_ACTION_NAME"),
            translator.Translator().translate(
                "MENU_BAR_TOGGLE_THEME_ACTION_STATUS_TIP"
            ),
            lambda: mainwindow.toggle_theme(),
            "toggle",
        )

        self.login_action = Action(
            translator.Translator().translate("MENU_BAR_LOGIN_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_LOGIN_ACTION_STATUS_TIP"),
            lambda: mainwindow.login(),
            "login",
        )

        self.logout_action = Action(
            translator.Translator().translate("MENU_BAR_LOGOUT_ACTION_NAME"),
            translator.Translator().translate("MENU_BAR_LOGOUT_ACTION_STATUS_TIP"),
            lambda: mainwindow.logout(),
            "logout",
        )

        self.language_menu = QtWidgets.QMenu(
            translator.Translator().translate("MENU_BAR_LANGUAGES_MENU")
        )
        for lang in translator.Translator().languages():
            name = translator.Translator().getLangName(lang)
            self.addAction(
                Action(name, name, partial(mainwindow.updateTranslate, lang), None),
                self.language_menu,
            )

    def addAction(
        self, action: Action, menu: Optional[QtWidgets.QMenu] = None
    ) -> QtWidgets.QAction:
        qaction = QtWidgets.QAction(action.label, self)

        if action.img:
            qaction.setIcon(
                QtGui.QIcon(
                    os.path.join(
                        skippy.config.RESOURCES_FOLDER, self.theme, f"{action.img}.png"
                    )
                )
            )

        qaction.setStatusTip(action.statusTip)
        qaction.triggered.connect(action.func)

        if not menu:
            super().addAction(qaction)
        else:
            menu.addAction(qaction)

        return qaction

    def addMenu(
        self, qmenu: Union[str, QtWidgets.QMenu], menu: Optional[QtWidgets.QMenu] = None
    ) -> QtWidgets.QMenu:
        if type(qmenu) == str:
            qmenu = QtWidgets.QMenu(qmenu, self)

        if not menu:
            super().addMenu(qmenu)
        else:
            menu.addMenu(qmenu)

        return qmenu


class MenuBar(ActionBarBase, QtWidgets.QMenuBar):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(MenuBar, self).__init__(parent)
        self.initActions()

        self.file_menu = self.addMenu(
            translator.Translator().translate("MENU_BAR_FILE_MENU")
        )
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

        self.edit_menu = self.addMenu(
            translator.Translator().translate("MENU_BAR_EDIT_MENU")
        )
        self.addAction(self.undo_action, self.edit_menu)
        self.addAction(self.redo_action, self.edit_menu)
        self.edit_menu.addSeparator()
        self.addAction(self.cut_action, self.edit_menu)
        self.addAction(self.copy_action, self.edit_menu)
        self.addAction(self.paste_action, self.edit_menu)
        self.addAction(self.select_all_action, self.edit_menu)
        self.edit_menu.addSeparator()
        self.addAction(self.preview_action, self.edit_menu)

        self.settings_menu = self.addMenu(
            translator.Translator().translate("MENU_BAR_SETTINGS_MENU")
        )
        self.addAction(self.toggle_theme_action, self.settings_menu)
        self.settings_menu.addMenu(self.language_menu)
        self.settings_menu.addSeparator()
        self.addAction(self.login_action, self.settings_menu)
        self.addAction(self.logout_action, self.settings_menu)


class ToolBar(ActionBarBase, QtWidgets.QToolBar):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(ToolBar, self).__init__(parent)
        self.initActions()

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
        self.initActions()

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
