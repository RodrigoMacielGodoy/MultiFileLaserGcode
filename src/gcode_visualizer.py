import re

from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QWheelEvent
from PyQt5.QtWidgets import QGraphicsView, QWidget
from PyQt5.QtCore import Qt, QPoint

from list_data_model import ListDataModel
import config

def average(iterable):
    return sum(iterable)/len(iterable)

class GcodeVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = None
        self.__offset = QPoint(0, 0)
        self.__last_offset = QPoint(0, 0)
        self.__first_pos = None
        self.__scale = 1.0
        self.__gcodes = {}

        self.pen_thickness = {"G0": 1, "G1": 3}
        self.pen_line_style = {"G0": Qt.DashLine, "G1": Qt.SolidLine}
        self.setMouseTracking(True)

    def resetView(self) -> None:
        self.__offset = QPoint(0,0)
        self.__last_offset = QPoint(0,0)
        self.__scale = 1.0
        self.update()

    def setModel(self, model: ListDataModel) -> None:
        self.__model = model
        self.__model.dataChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.translate(self.__offset)
        painter.scale(self.__scale, self.__scale)

        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawLine(0, self.height(),
                        self.width(), self.height())

        painter.drawLine(0,0,
                        0, self.height())
        last_pt = {"point":(0,0)}
        speed = None
        for file in self.__model.items:
            if not file.showing_gcode:
                continue
            gcode = file.gcode
            if not gcode:
                continue
            try:
                points, power = self.parse_gcode(gcode)
            except Exception as ex:
                print(ex)
                continue
            
            for i,point in enumerate(points):
                if i > 0:
                    last_pt = points[i-1]
                start_pt = QPoint( int(10*last_pt["point"][0]), self.height() - int(10*last_pt["point"][1]))
                end_pt = QPoint( int(10*point["point"][0]), self.height() - int(10*point["point"][1]) )
                
                painter.setPen(QPen(self.power_color(power*file.passes,
                                                     (0, config.LASER_POWER/config.MIN_FEED_RATE),
                                                     reverse=True),
                                    self.pen_thickness[point["cmd"]],
                                    self.pen_line_style[point["cmd"]]))
                painter.drawLine(start_pt, end_pt)
            last_pt = points[-1]


    def parse_gcode(self, gcode) -> tuple:
        power = re.findall("M4\s*S(\d+)", gcode)
        points = []
        speeds = []
        if len(power) > 0:
            power = int(power[0])
        for line in gcode.split("\n"):
            cmd = re.findall("(G[0,1])", line)
            if len(cmd) == 0:
                continue
            pt_data = {
                "cmd": cmd[0]
            }

            point = re.findall("X(-*\d+\.*\d*)\s*Y(-*\d+\.*\d*)", line)[0]
            pt_data["point"] = (float(point[0]), float(point[1]))

            speed = re.findall("F(\d+)", line)
            if len(speed) > 0:
                speeds.append(int(speed[0]))

            points.append(pt_data)
        
        speed = sum(speeds)/len(speeds)

        power = ((power/255.0)*config.LASER_POWER)/speed
        return (points, power)

    def power_color(self, power: int, range: tuple, reverse: bool=False) -> QColor:
        min_ = range[0]
        max_ = range[1]
        if power <= int((min_+max_)/2):
            r = 255
            g = min(int(255*power/int((min_+max_)/2)), 255)
            b = 0
        else:
            r = min(int(255*(max_-power)/int((min_+max_)/2)), 255)
            g = 255
            b = 0
        if reverse:
            r, g = g, r

        return QColor("#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in (r, g, b)]))

    def wheelEvent(self, event: QWheelEvent) -> None:
        val = event.angleDelta().y()//120
        factor = 0.2
        self.__scale += val*factor
        if self.__scale <= 0.2:
            self.__scale = 0.2
            self.update()
            return
        if self.__scale >= 1.8:
            self.__scale = 1.8
            self.update()
            return

        pos = event.position()
        self.__last_offset = self.__offset
        self.__offset += val*(self.__offset - pos)*factor
        self.update()

    def mouseReleaseEvent(self, evt) -> None:
        self.__first_pos = None
        self.__last_offset = self.__offset

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if not self.__first_pos:
                self.__first_pos = event.localPos()
                return
            self.__offset = self.__last_offset - self.__first_pos + event.localPos()
            self.update()