import re
import traceback

from PyQt5.QtCore import QPoint, QPointF, QPropertyAnimation, Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QWheelEvent
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget

import config
from list_data_model import ListDataModel


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

        self.__gcode_scale = 10
        self.__near_range = 10
        self.__draw_points = []
        self.__circ_radius = 3
        self.pen_thickness = {"G0": 1, "G1": 3}
        self.pen_line_style = {"G0": Qt.DashLine, "G1": Qt.SolidLine}

        self.redraw = True
        self.__cache = {}
        self.__drew = []

        self.__lb_pos = QLabel(self)
        self.__lb_lock_pos = QPoint(0,0)
        self.__lb_pos.setStyleSheet("QLabel{color:white;background:black;}")
        self.__lb_offset = QPoint(20,20)
        self.__lb_effect = QGraphicsOpacityEffect()
        self.__lb_pos.setGraphicsEffect(self.__lb_effect)
        self.__lb_fade_anim = QPropertyAnimation(self.__lb_effect, b"opacity")
        self.__lb_fade_anim.setDuration(800)
        self.__lb_fade_anim.setStartValue(1.0)
        self.__lb_fade_anim.setEndValue(0.2)
        self.__lb_fade_anim.finished.connect(self.__lb_pos.hide)
        
        self.setMouseTracking(True)

    def resetView(self) -> None:
        self.__offset = QPoint(0,0)
        self.__last_offset = QPoint(0,0)
        self.__scale = 1.0
        self.update()

    def setModel(self, model: ListDataModel) -> None:
        self.__model = model
        self.__model.dataChanged.connect(self.data_changed)

    def data_changed(self, data: list) -> None:
        self.redraw = True
        self.update()

    def qpoint_to_tuple(self, qpoint: "QPoint | QPointF") -> tuple:
        return (qpoint.x(), qpoint.y())

    def paintEvent(self, event):
        self.__draw_points.clear()
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.translate(self.__offset)
        painter.scale(self.__scale, self.__scale)


        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.drawLine(0, self.height(),
                        self.width(), self.height())

        if self.redraw:
            self.redraw = False
            painter.drawLine(0,0,
                            0, self.height())
            last_pt = {"point":(0,0)}
            self.__cache["lines"] = []
            self.__cache["pens"] = []
            for file in self.__model.items:
                if not file.showing_gcode:
                    continue
                gcode = file.gcode
                if not gcode:
                    continue
                try:
                    points, power = self.parse_gcode(gcode)
                    if points is None and power is None:
                        continue
                except Exception as ex:
                    print(traceback.print_exc())
                    continue
                
                for i,point in enumerate(points):
                    if i > 0:
                        last_pt = points[i-1]
                    start_pt = QPointF(self.__gcode_scale*last_pt["point"][0],
                                    self.height() - self.__gcode_scale*last_pt["point"][1])
                    end_pt = QPointF(self.__gcode_scale*point["point"][0],
                                    self.height() - self.__gcode_scale*point["point"][1])

                    pen = QPen(self.power_color(power*file.passes,
                                (0, config.LASER_POWER/config.MIN_FEED_RATE),
                                reverse=True),
                                self.pen_thickness[point["cmd"]],
                                self.pen_line_style[point["cmd"]])

                    self.__draw_points.append(end_pt)
                    self.__cache["lines"].append((start_pt, end_pt))
                    self.__cache["pens"].append(pen)
                    painter.setPen(pen)
                    painter.drawLine(start_pt, end_pt)
                    painter.drawEllipse(QPointF(end_pt), self.__circ_radius, self.__circ_radius)
                last_pt = points[-1]
        else:
            k = 0
            self.__drew[:] = []
            for i,line in enumerate(self.__cache["lines"]):
                line_tuple = [self.qpoint_to_tuple(line[i]) for i in range(len(line))]
                if line_tuple in self.__drew:
                    break
                self.__drew.append(line_tuple)
                painter.setPen(self.__cache["pens"][i])
                painter.drawLine(line[0], line[1])
                painter.drawEllipse(line[1], self.__circ_radius, self.__circ_radius)

    def parse_gcode(self, gcode) -> tuple:
        if gcode == "":
            return None, None
        power = re.findall("M4\s*S(\d+)", gcode)
        points = []
        speeds = []
        cmds = []
        if len(power) > 0:
            power = int(power[0])
        for line in gcode.split("\n"):
            cmd = re.findall("(G[0,1])", line)
            if len(cmd) == 0:
                continue

            point = re.findall("X(-*\d+\.*\d*)\s*Y(-*\d+\.*\d*)", line)[0]
            cmd_line = " ".join(cmd+list(point))

            if cmd_line in cmds:
                break

            cmds.append(cmd_line)

            pt_data = {
                "cmd": cmd[0],
                "point":(float(point[0]), float(point[1]))
            }
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
        n_scale = self.__scale + (val*factor)
        pos = event.position()

        if n_scale <= 0.2:
            n_scale = 0.2
            self.update()
            return
        if n_scale >= 1.8:
            n_scale = 1.8
            self.update()
            return

        n_offset = self.__offset + (val*factor*(self.__offset - pos))

        if not self.__lb_pos.isHidden():
            self.__lb_pos.hide()
        
        self.__last_offset = self.__offset
        self.__offset = n_offset
        self.__scale = n_scale
        self.update()

    def mouseReleaseEvent(self, evt) -> None:
        self.__first_pos = None
        self.__last_offset = self.__offset

    def enterEvent(self, a0) -> None:
        self.__lb_pos.show()
        self.__lb_effect.setOpacity(1.0)
        self.__lb_fade_anim.stop()
        return super().enterEvent(a0)

    def leaveEvent(self, a0) -> None:
        self.__lb_fade_anim.start()
        return super().leaveEvent(a0)

    def mouseMoveEvent(self, event):
        for pt in self.__draw_points:
            local_pt = (pt*self.__scale)+self.__offset
            diff = local_pt-event.pos()
            dist = diff.manhattanLength()
            if dist <= self.__near_range:
                d_pt = QPointF(
                    pt.x()/self.__gcode_scale,
                    (self.height()-pt.y())/self.__gcode_scale
                )
                self.__lb_pos.setText(f"X {d_pt.x():0.3f}; "
                                        f"Y {d_pt.y():0.3f}")
                self.__lb_pos.adjustSize()
                self.__lb_pos.show()
                self.__lb_pos.move(QPoint(int(local_pt.x()), int(local_pt.y())))
                self.__lb_lock_pos = local_pt

        if event.buttons() == Qt.LeftButton:
            if not self.__first_pos:
                self.__first_pos = event.localPos()
                return
            self.__offset = self.__last_offset - self.__first_pos + event.localPos()
            if not self.__lb_pos.isHidden():
                self.__lb_pos.hide()
                # n_pos = (self.__lb_lock_pos*self.__scale) + self.__offset
                # self.__lb_pos.move((n_pos).toPoint())
            self.update()
