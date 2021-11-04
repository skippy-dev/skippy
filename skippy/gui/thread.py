from PyQt5 import QtCore


class AbstractWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def run(self):
        raise NotImplementedError


class Thread(QtCore.QThread):
    def __init__(self, worker: AbstractWorker):
        super(Thread, self).__init__()
        self.worker = worker
        self.worker.moveToThread(self)

        self.worker.finished.connect(self.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.started.connect(self.worker.run)
        self.finished.connect(self.deleteLater)
