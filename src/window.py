import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from main_window_layout import Ui_MainWindow as WindowLayout

from file_config_widget import FileConfigWidget
from list_data_model import ListDataModel

# TODO: create beahavior for open Folder
# TODO: Add file filter to the config to be used in drop-down and open files behavior
# TODO: Add save project
# TODO: Add configurations Window
# TODO: Add materials settings (sqlite (?))
# TODO: Add start and end Gcodes for each File

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = WindowLayout()
        self.filesDataModel = ListDataModel()
        self.showing_all_gcode = True
        self.setupUI()
        self.setupConnects()

    def setupUI(self) -> None:
        self.ui.setupUi(self)
        self.ui.dropableListWidget.setModel(self.filesDataModel)
        self.ui.graphicsView.setModel(self.filesDataModel)
        self.ui.bt_add_new_dir.hide()

    def setupConnects(self) -> None:
        self.ui.dropableListWidget.newFilesDropped.connect(self.newFilesDropped)
        self.ui.bt_reset_view.clicked.connect(self.resetGcodeView)
        self.ui.bt_generate_gcode.clicked.connect(self.filesDataModel.generateGcodes)
        self.ui.bt_save_gcode.clicked.connect(self.save_gcode)
        self.ui.bt_delete_all.clicked.connect(self.delete_all_svgs)
        self.ui.bt_hide_show_all.clicked.connect(self.hide_show_all_svgs)
        self.ui.bt_add_file.clicked.connect(self.open_file)

    def open_file(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose a file",
                                                os.path.expanduser("~"),
                                                "Files (*.svg)")
        if not paths:
            return
        self.newFilesDropped(paths)

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

    def save_gcode(self) -> None:
        path = QFileDialog.getSaveFileName(self, "", os.path.expanduser("~"))
        if path:
            with open(path[0], "w") as f:
                for file in self.filesDataModel.items:
                    f.write(file.gcode+"\n")

    def delete_all_svgs(self) -> None:
        self.filesDataModel.clearItems()

    def hide_show_all_svgs(self) -> None:
        for fileWidget in self.filesDataModel.items:
            fileWidget.showing_gcode = self.showing_all_gcode
            fileWidget.hide_show_gcode()

        self.showing_all_gcode = not self.showing_all_gcode

        if self.showing_all_gcode:
            self.ui.bt_hide_show_all.setIcon(QIcon(":/icons/Media/Icons/eye-outline.svg"))
        else:
            self.ui.bt_hide_show_all.setIcon(QIcon(":/icons/Media/Icons/eye-off-outline.svg"))
            