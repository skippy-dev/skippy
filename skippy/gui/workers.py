from PyQt5 import QtCore

from skippy.api import PageData

from skippy.core import scpclient

from skippy.gui import thread, utils

from skippy.utils import discord_rpc

from typing import List
import os


class FileWorker(thread.AbstractWorker):
    progress = QtCore.pyqtSignal(str, bytes)

    def __init__(self, files: List[str]):
        super(FileWorker, self).__init__()
        self.files = files

    def run(self):
        for file in self.files:
            if file:
                with open(file, "rb") as f:
                    self.progress.emit(os.path.split(file)[1], f.read())
        self.finished.emit()


class UploadWorker(thread.AbstractWorker):
    def __init__(self, pdata: PageData, comment: str = "Edit using Skippy"):
        super(UploadWorker, self).__init__()
        self.pdata = pdata
        self.comment = comment

    def run(self):
        scpclient.SCPClient().upload(self.pdata, self.comment)
        self.finished.emit()


class DiscordRPCWorker(thread.AbstractWorker):
    def __init__(self, title: str, words: int, letters: int):
        super(DiscordRPCWorker, self).__init__()
        self.rpc = discord_rpc.DiscordRPC()

        self.title = title
        self.words = words
        self.letters = letters

    def run(self):
        self.rpc.update(self.title, self.words, self.letters)

        self.finished.emit()
