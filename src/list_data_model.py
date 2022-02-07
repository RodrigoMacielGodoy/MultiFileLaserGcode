from PyQt5.QtCore import QObject, pyqtSignal
from file_config_widget import FileConfigWidget

class ListDataModel(QObject):
    dataChanged = pyqtSignal(list)
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.__data = []
        self.__paths = []

    @property
    def items(self) -> list:
        return self.__data

    def __emit_change(self) -> None:
        self.dataChanged.emit(self.__data)

    def addItem(self, item: FileConfigWidget) -> None:
        if item.path in self.__paths:
            return
        self.__paths.append(item.path)
        item.upPressed.connect(self.moveItemUp)
        item.downPressed.connect(self.moveItemDown)
        item.dataChanged.connect(self.__emit_change)
        self.__data.insert(0, item)
        self.dataChanged.emit(self.__data)

    def removeItem(self, item) -> None:
        path = item.path
        if item in self.__data:
            if item.path in self.__paths:
                self.__paths.remove(item.path)
            self.__data.remove(item)
            item.setParent(None)
            del(item)
        self.dataChanged.emit(self.__data)

    def moveItemUp(self, item) -> None:
        index = self.__data.index(item)
        if index-1 < 0:
            return
        self.__data[index-1], self.__data[index] = self.__data[index], self.__data[index-1]
        self.dataChanged.emit(self.__data)

    def moveItemDown(self, item) -> None:
        index = self.__data.index(item)
        if index+1 >= len(self.__data):
            return
        self.__data[index+1], self.__data[index] = self.__data[index], self.__data[index+1]
        self.dataChanged.emit(self.__data)

    def generateGcodes(self) -> None:
        for item in self.__data:
            item.generate_gcode()

    def sort(self, reverse: bool = False) -> None:
        self.__data.sort(key=lambda x: x.file_name)
        if reverse:
            self.__data.reverse()
        self.dataChanged.emit(self.__data)