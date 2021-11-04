from skippy.gui import CriticalMessageBox

from skippy.utils.logger import log

import traceback
import sys


def excepthook(exc_type, value, tb):
    exc = "".join(traceback.format_exception(exc_type, value, tb))
    log.error(exc)
    CriticalMessageBox(f'{exc_type.__name__}: {value}', exc).exec_()


def init():
    sys.excepthook = excepthook
