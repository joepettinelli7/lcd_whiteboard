"""
    LCD Whiteboard to create touchscreen whiteboard interface and send MMS.
    Copyright (C) 2025 Joseph Pettinelli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see https://www.gnu.org/licenses/.
"""

import os
import typing
from PyQt5.QtCore import Qt, QPoint, QLine
from PyQt5.QtGui import QPainter, QPen, QPaintEvent, QMouseEvent, QColor, QPixmap
from PyQt5.QtWidgets import QFrame

from src.server_side.app import ROOT_DIR
from src.server_side.backend.lines.line import ColorLine
from src.server_side.backend.lines.line_list import LineList
from src.server_side.backend.configs.drawing_surface_config import DrawingSurfaceConfig
from src.server_side.backend.configs.drawing_surface_config import DARK_KEY

IMAGE_PATH: str = os.path.join(ROOT_DIR, 'src', 'client_side', 'static')
IMAGE_NAME = 'wb_image.png'


class DrawingSurface(QFrame):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._config: DrawingSurfaceConfig = DrawingSurfaceConfig()
        self._all_lines: LineList = LineList()
        self._current_line: ColorLine = ColorLine()
        self._selected_color: QColor = QColor('black')
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)
        self.apply_config()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Called when user clicks mouse.
        Need to add single point here to make dot.

        Args:
            event: A QMouseEvent by user

        Returns:

        """
        if event.button() == Qt.LeftButton:
            new_point = event.pos()
            self._current_line.add_point(new_point)
            self._current_line.color = self._selected_color
        else:
            return

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Called when user releases mouse

        Args:
            event: A QMouseEvent by user

        Except:
            AssertionError if no points appended

        Returns:

        """
        if event.button() == Qt.LeftButton:
            try:
                assert len(self._current_line.points) > 0
                current_line_copy = self._current_line.make_copy()
                self._all_lines.add_line(current_line_copy)
                self._current_line.points.clear()
            except AssertionError:
                self.handle_no_points_error()
        else:
            return

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Called when user moves mouse

        Args:
            event: A QMouseEvent by user

        Returns:

        """
        if event.buttons() & Qt.LeftButton:
            new_point = event.pos()
            self._current_line.add_point(new_point)
        else:
            return

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint on the widget during and after mouse events.
        Can draw dot or line.

        Args:
            event: A paint event

        Returns:

        """
        painter = QPainter(self)
        try:
            # Paint current line
            self.paint_line(self._current_line, painter)
            # Paint previous lines
            for color_line in self._all_lines.line_list:
                self.paint_line(color_line, painter)
        except AssertionError:
            self.handle_no_points_error()
        self.update()
        painter.end()

    def paint_line(self, color_line: ColorLine, painter: QPainter) -> None:
        """
        Paint single line

        Args:
            color_line: The line or lines to paint
            painter: The painter to use for line

        Returns:

        """
        pen = QPen(color_line.color, 2)
        if len(color_line.points) == 0:
            return
        elif len(color_line.points) == 1:
            pen.setStyle(Qt.DotLine)
            painter.setPen(pen)
            painter.drawPoint(color_line.points[0])
        else:
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)
            for line in self.line_generator(color_line.points):
                # Need to draw line because points are too far
                # apart when user moves mouse too fast
                painter.drawLine(line)

    @staticmethod
    def line_generator(point_list: typing.List[QPoint]):
        """
        Yield the line resulting from a point and next point

        Args:
            point_list: Points to iterate over

        Yields:
             The line to draw
        """
        assert len(point_list) > 1
        for i, point in enumerate(point_list[:-1]):
            next_point = point_list[i + 1]
            line = QLine(point, next_point)
            yield line

    @staticmethod
    def handle_no_points_error() -> None:
        """
        Handle error if no points after mouse release event

        Returns:

        """
        print("\nNo points appended during mouse move!")

    def save_whiteboard_image(self) -> bool:
        """
        Save the current whiteboard pixmap to client/static/wb_image.png
        so that the twilio API can send it using public URL

        Returns:
             True if image saved, False if image not saved
        """
        pixmap = self.get_whiteboard_pixmap()
        if not os.path.exists(IMAGE_PATH):
            os.mkdir(IMAGE_PATH)
        save_success = pixmap.save(IMAGE_PATH + IMAGE_NAME, "PNG")
        return save_success

    def get_whiteboard_pixmap(self) -> QPixmap:
        """
        Get the image currently on the drawing surface

        Returns:
             The image
        """
        rect = self.rect()
        pixmap = self.grab(rect)
        return pixmap

    @staticmethod
    def delete_wb_image() -> None:
        """
        Delete wb_image when app closes

        Returns:

        """
        if os.path.exists(IMAGE_PATH + IMAGE_NAME):
            os.remove(IMAGE_PATH + IMAGE_NAME)

    def undo_line_slot(self) -> None:
        """
        Undo the last line that was drawn

        Returns:

        """
        try:
            self._all_lines.line_list.pop()
            self.update()
        except IndexError:
            # No lines
            pass

    def toggle_dark_slot(self) -> None:
        """
        Toggle drawing surface dark mode

        Returns:

        """
        dark_mode = not self._config[DARK_KEY]
        color = "black" if dark_mode else "white"
        self.setStyleSheet(f"background-color: {color};")
        self._all_lines.invert_lines_colors()
        self._config[DARK_KEY] = dark_mode
        self.update()

    def apply_config(self) -> None:
        """
        Apply the loaded config

        Returns:

        """
        dark_mode = self._config[DARK_KEY]
        color = "black" if dark_mode else "white"
        self.setStyleSheet(f"background-color: {color};")
        self.update()

    def save_config(self) -> None:
        """
        Save the drawing surface config
        to a file on disk

        Returns:

        """
        self._config.save()

    @property
    def center(self) -> QPoint:
        """
        The center of drawing surface widget

        Returns:
             Center point
        """
        geom = self.geometry()
        center_x = geom.left() + geom.width() // 2
        center_y = geom.top() + geom.height() // 2
        return QPoint(center_x, center_y)

    @property
    def selected_color(self) -> QColor:
        """
        The current color set to pen

        Returns:
             The color
        """
        return self._selected_color

    @selected_color.setter
    def selected_color(self, new_color: QColor) -> None:
        """
        Set the current color to be used by pen

        Returns:

        """
        assert isinstance(new_color, QColor)
        if new_color.isValid():
            self._selected_color = new_color
        else:
            pass


if __name__ == "__main__":
    pass
