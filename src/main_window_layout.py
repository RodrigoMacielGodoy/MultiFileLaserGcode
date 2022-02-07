# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = GcodeVisualizer(self.tab)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 2, 2, 1)
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setMaximumSize(QtCore.QSize(370, 16777215))
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bt_add_new_dir = QtWidgets.QPushButton(self.frame)
        self.bt_add_new_dir.setMaximumSize(QtCore.QSize(90, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/folder-add-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_add_new_dir.setIcon(icon)
        self.bt_add_new_dir.setObjectName("bt_add_new_dir")
        self.horizontalLayout.addWidget(self.bt_add_new_dir)
        self.bt_add_file = QtWidgets.QPushButton(self.frame)
        self.bt_add_file.setMaximumSize(QtCore.QSize(90, 16777215))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/file-add-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_add_file.setIcon(icon1)
        self.bt_add_file.setObjectName("bt_add_file")
        self.horizontalLayout.addWidget(self.bt_add_file)
        self.bt_hide_show_all = QtWidgets.QPushButton(self.frame)
        self.bt_hide_show_all.setMaximumSize(QtCore.QSize(90, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/eye-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_hide_show_all.setIcon(icon2)
        self.bt_hide_show_all.setObjectName("bt_hide_show_all")
        self.horizontalLayout.addWidget(self.bt_hide_show_all)
        self.bt_delete_all = QtWidgets.QPushButton(self.frame)
        self.bt_delete_all.setMaximumSize(QtCore.QSize(90, 16777215))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/trash-2-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_delete_all.setIcon(icon3)
        self.bt_delete_all.setObjectName("bt_delete_all")
        self.horizontalLayout.addWidget(self.bt_delete_all)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.bt_reset_view = QtWidgets.QPushButton(self.tab)
        self.bt_reset_view.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/home-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_reset_view.setIcon(icon4)
        self.bt_reset_view.setIconSize(QtCore.QSize(16, 16))
        self.bt_reset_view.setObjectName("bt_reset_view")
        self.horizontalLayout_2.addWidget(self.bt_reset_view)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(370, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(370, 16777215))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.dropableListWidget = DropableListWidget()
        self.dropableListWidget.setGeometry(QtCore.QRect(0, 0, 368, 461))
        self.dropableListWidget.setObjectName("dropableListWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dropableListWidget)
        self.verticalLayout_2.setContentsMargins(5, -1, 5, 12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(20, 154, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.scrollArea.setWidget(self.dropableListWidget)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 2)
        self.bt_generate_gcode = QtWidgets.QPushButton(self.tab)
        self.bt_generate_gcode.setMinimumSize(QtCore.QSize(0, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/arrow-down-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_generate_gcode.setIcon(icon5)
        self.bt_generate_gcode.setObjectName("bt_generate_gcode")
        self.gridLayout.addWidget(self.bt_generate_gcode, 2, 0, 1, 1)
        self.bt_save_gcode = QtWidgets.QPushButton(self.tab)
        self.bt_save_gcode.setMinimumSize(QtCore.QSize(0, 40))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/Media/Icons/download-outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_save_gcode.setIcon(icon6)
        self.bt_save_gcode.setObjectName("bt_save_gcode")
        self.gridLayout.addWidget(self.bt_save_gcode, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MultiGcoder"))
        self.bt_add_new_dir.setText(_translate("MainWindow", "Folder..."))
        self.bt_add_file.setText(_translate("MainWindow", "File..."))
        self.bt_hide_show_all.setText(_translate("MainWindow", "All"))
        self.bt_delete_all.setText(_translate("MainWindow", "All"))
        self.bt_generate_gcode.setText(_translate("MainWindow", "Generate Gcode"))
        self.bt_save_gcode.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "GCode Gen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Sender"))
from dropable_list import DropableListWidget
from gcode_visualizer import GcodeVisualizer
import icons_rc
