import os
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5 import QtCore

from list_data_model import ListDataModel

class DropableListWidget(QWidget):
    newFilesDropped = QtCore.pyqtSignal(list)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.__model = None
        self.accepted_exts = [".svg"]

    def setModel(self, model: ListDataModel) -> None:
        self.__model = model
        self.__model.dataChanged.connect(self.updateLayout)

    def updateLayout(self, newData: list) -> None:
        layout = self.layout()
        for i, item in enumerate(newData):
            layout.removeWidget(item)
            layout.insertWidget(i, item)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        urls = [u.toLocalFile() for u in event.mimeData().urls()]
        files = []
        for path in urls:
            if os.path.isfile(path):
                files.append(path)
            elif os.path.isdir(path):
                files += [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(path+f)]

        if len(self.accepted_exts) > 0:
            files = [f for f in files if os.path.splitext(f)[1] in self.accepted_exts]

        self.newFilesDropped.emit(files)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()