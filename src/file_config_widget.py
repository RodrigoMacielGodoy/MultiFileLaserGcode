from importlib.resources import path
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QIcon
from svg_to_gcode.compiler import Compiler
from svg_to_gcode.svg_parser import parse_file

from file_config_widget_layout import Ui_Form as WidgetLayout
from laser_gcode_interface import LaserInterface


class FileConfigWidget(QWidget):
    upPressed = pyqtSignal(QWidget)
    downPressed = pyqtSignal(QWidget)
    dataChanged = pyqtSignal()

    def __init__(self, path: str, parent = None) -> None:
        super().__init__(parent)
        self.path = path
        self.file_name = os.path.basename(path)
        
        self.ui = WidgetLayout()
        self.feed_rate = 600
        self.laser_power = 0.5
        self.passes = 1
        self.power_coef = 0
        self.gcode = ""
        self.curves = []
        self.showing_gcode = True
        self.__valid_file = None
        self.setupUI()
        self.setupConnects()
        self.power_coef_changed()

    def setupUI(self) -> None:
        self.ui.setupUi(self)
        self.ui.bt_top_generate_gcode.hide()

        self.ui.groupBox.setTitle(self.file_name)
        self.ui.bt_move_up.clicked.connect(self.__emit_move_up)
        self.ui.bt_move_down.clicked.connect(self.__emit_move_down)

        self.ui.le_feed_rate.setValidator(QIntValidator(self.ui.le_feed_rate))
        self.ui.le_passes.setValidator(QIntValidator(self.ui.le_passes))
        self.ui.le_power.setValidator(QDoubleValidator(0.0, 1.0, 2))

        self.ui.le_feed_rate.setText(str(self.feed_rate))
        self.ui.le_power.setText(str(self.laser_power))
        self.ui.le_passes.setText(str(self.passes))
        self.ui.hs_power.setValue(self.laser_power*100)

    def setupConnects(self) -> None:
        self.ui.le_feed_rate.textChanged.connect(self.feed_rate_changed)
        self.ui.le_power.textChanged.connect(self.laser_power_changed)
        self.ui.hs_power.valueChanged.connect(self.laser_power_changed)
        self.ui.le_passes.textChanged.connect(self.passes_changed)
        self.ui.bt_reload_gcode.clicked.connect(self.generate_gcode)
        self.ui.bt_top_generate_gcode.clicked.connect(self.ui.bt_reload_gcode.clicked.emit)

        self.ui.bt_hide_show_gcode.clicked.connect(self.hide_show_gcode)

        self.ui.groupBox.toggled.connect(self.hide_show_config)

    def update_gcode_show_button(self) -> None:
        if self.showing_gcode:
            self.ui.bt_hide_show_gcode.setIcon(QIcon(":/icons/Media/Icons/eye-outline.svg"))
        else:
            self.ui.bt_hide_show_gcode.setIcon(QIcon(":/icons/Media/Icons/eye-off-outline.svg"))

    def __emit_move_up(self) -> None:
        self.upPressed.emit(self)

    def __emit_move_down(self) -> None:
        self.downPressed.emit(self)

    def hide_show_config(self, checked: bool) -> None:
        if checked:
            self.ui.bt_top_generate_gcode.hide()
            self.ui.config_frame.show()
            self.setMaximumHeight(500)
        else:
            self.ui.bt_delete_file.setEnabled(True)
            self.ui.bt_move_down.setEnabled(True)
            self.ui.bt_move_up.setEnabled(True)
            self.ui.bt_hide_show_gcode.setEnabled(True)
            self.ui.bt_top_generate_gcode.show()
            self.ui.bt_top_generate_gcode.setEnabled(True)
            self.ui.config_frame.hide()
            self.setMaximumHeight(60)

    def hide_show_gcode(self) -> None:
        self.showing_gcode = not self.showing_gcode
        self.dataChanged.emit()
        self.update_gcode_show_button()

    def feed_rate_changed(self, val: str) -> None:
        if val != "":
            self.feed_rate = int(val)
            if self.feed_rate <= 0:
                self.feed_rate = 1
            self.power_coef_changed()
    
    def laser_power_changed(self, val: "str | int") -> None:
        updt_le = False
        if val == "":
            val = 0

        if type(val) is str:
            self.ui.le_power.blockSignals(True)
            self.ui.hs_power.blockSignals(True)
            val = min(float(val)/100.0, 1.0)
            self.ui.hs_power.setValue(val*100)
            self.ui.le_power.blockSignals(False)
            self.ui.hs_power.blockSignals(False)
        elif type(val) is int:
            self.ui.le_power.blockSignals(True)
            val = val/100.0
            self.ui.le_power.setText(str(val))
            self.ui.le_power.blockSignals(False)

        self.laser_power = val
        self.power_coef_changed()

    def passes_changed(self, val: str) -> None:
        if val != "":
            self.passes = int(val)
            self.power_coef_changed()

    def power_coef_changed(self) -> None:
        self.power_coef = (self.laser_power/self.feed_rate)*self.passes*100
        self.ui.lb_power_coef.setText(f"Power Coef.: {self.power_coef:0.2f}")

    def generate_gcode(self) -> None:
        compiler = Compiler(LaserInterface,
                            movement_speed=self.feed_rate,
                            cutting_speed=self.feed_rate,
                            pass_depth=0,
                            laser_power=self.laser_power,
                            laser_mode=True,
                            custom_header=[LaserInterface().set_laser_power(self.laser_power)],
                            custom_footer=["M5"])
        try:
            self.curves = parse_file(self.path)
            compiler.append_curves(self.curves)
            self.gcode = compiler.compile(passes=self.passes)
        except:
            self.__valid_file = False
            return
        self.__valid_file = True
        self.dataChanged.emit()