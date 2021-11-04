######################################################################
### From https://github.com/gmarull/qtmodern
######################################################################

from PyQt5 import QtGui

from skippy.gui import utils

import skippy.config

import os

_STYLESHEET = os.path.join(skippy.config.RESOURCES_FOLDER, "stylesheet", "style.qss")
""" str: Main stylesheet. """


def _apply_base_theme(app):
    """Apply base theme to the application.
    Args:
            app (QApplication): QApplication instance.
    """

    app.setStyle("Fusion")

    with open(_STYLESHEET) as stylesheet:
        app.setStyleSheet(stylesheet.read())


def dark():
    """Apply Dark Theme to the Qt application instance."""
    app = utils.getApplication()

    darkPalette = QtGui.QPalette()

    # base
    darkPalette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.Light, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.Midlight, QtGui.QColor(90, 90, 90))
    darkPalette.setColor(QtGui.QPalette.Dark, QtGui.QColor(35, 35, 35))
    darkPalette.setColor(QtGui.QPalette.Text, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(42, 42, 42))
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(20, 20, 20))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(56, 252, 196))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(66, 66, 66))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(180, 180, 180))
    darkPalette.setColor(QtGui.QPalette.LinkVisited, QtGui.QColor(80, 80, 80))

    # disabled
    darkPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(127, 127, 127)
    )
    darkPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(127, 127, 127)
    )
    darkPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(127, 127, 127)
    )
    darkPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80)
    )
    darkPalette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.HighlightedText,
        QtGui.QColor(127, 127, 127),
    )

    app.setPalette(darkPalette)

    _apply_base_theme(app)


def light():
    """Apply Light Theme to the Qt application instance."""
    app = utils.getApplication()

    lightPalette = QtGui.QPalette()

    # base
    lightPalette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(240, 240, 240))
    lightPalette.setColor(QtGui.QPalette.Light, QtGui.QColor(180, 180, 180))
    lightPalette.setColor(QtGui.QPalette.Midlight, QtGui.QColor(200, 200, 200))
    lightPalette.setColor(QtGui.QPalette.Dark, QtGui.QColor(225, 225, 225))
    lightPalette.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(237, 237, 237))
    lightPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
    lightPalette.setColor(QtGui.QPalette.Shadow, QtGui.QColor(20, 20, 20))
    lightPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(76, 163, 224))
    lightPalette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(0, 162, 232))
    lightPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(225, 225, 225))
    lightPalette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(240, 240, 240))
    lightPalette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0))
    lightPalette.setColor(QtGui.QPalette.LinkVisited, QtGui.QColor(222, 222, 222))

    # disabled
    lightPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(115, 115, 115)
    )
    lightPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(115, 115, 115)
    )
    lightPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(115, 115, 115)
    )
    lightPalette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(190, 190, 190)
    )
    lightPalette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.HighlightedText,
        QtGui.QColor(115, 115, 115),
    )

    app.setPalette(lightPalette)

    _apply_base_theme(app)
