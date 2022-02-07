from PyQt5.QtWidgets import QMainWindow
from main_window_layout import Ui_MainWindow as WindowLayout

from file_config_widget import FileConfigWidget
from list_data_model import ListDataModel

# TODO: create beahaviors for the open File, Folder buttons,
# Delete All and Show/Hide all buttons.
# TODO: Add save project
# TODO: Add configurations Window
# TODO: Add materials settings (sqlite (?))
# TODO: Add start and end Gcodes for each File

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = WindowLayout()
        self.filesDataModel = ListDataModel()
        self.setupUI()
        self.setupConnects()

    def setupUI(self) -> None:
        self.ui.setupUi(self)
        self.ui.dropableListWidget.setModel(self.filesDataModel)
        self.ui.graphicsView.setModel(self.filesDataModel)

    def setupConnects(self) -> None:
        self.ui.dropableListWidget.newFilesDropped.connect(self.newFilesDropped)
        self.ui.bt_reset_view.clicked.connect(self.resetGcodeView)
        self.ui.bt_generate_gcode.clicked.connect(self.filesDataModel.generateGcodes)

    def newFilesDropped(self, files: list) -> None:
        for file in files:
            item = FileConfigWidget(file)
            self.addFileItem(item)
        self.sortFilesWidgets()

    def addFileItem(self, item) -> None:
        item.ui.bt_delete_file.clicked.connect(lambda: self.filesDataModel.removeItem(item))
        self.filesDataModel.addItem(item)

    def sortFilesWidgets(self) -> None:
        self.filesDataModel.sort()
    
    def resetGcodeView(self) -> None:
        self.ui.graphicsView.resetView()