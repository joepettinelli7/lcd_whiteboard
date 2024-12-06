import typing
import copy

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

L = typing.TypeVar('L', bound='Line')
CL = typing.TypeVar('CL', bound='ColorLine')


class Line:

    def __init__(self) -> None:
        super().__init__()
        self._points: typing.List[QPoint] = []

    @property
    def points(self) -> typing.List[QPoint]:
        """

        Returns:
             The points comprising the line
        """
        return self._points

    def make_straight(self) -> None:
        """
        Make the line straight

        Returns:

        """
        if len(self._points) > 2:
            self._points = [self._points[0], self._points[-1]]
        else:
            pass

    def add_points(self, points: typing.List[typing.Union[QPoint, typing.Tuple[int, int]]]) -> None:
        """
        Add multiple points to a line

        Args:
            points: The points to add

        Returns:

        """
        assert isinstance(points, list)
        for point in points:
            self.add_point(point)

    def add_point(self, point: typing.Union[QPoint, typing.Tuple[int, int]]) -> None:
        """
        Add a point to line

        Args:
            point: The point to add

        Returns:

        """
        if isinstance(point, QPoint):
            self._points.append(point)
        else:
            assert isinstance(point[0], int)
            assert isinstance(point[1], int)
            p = QPoint(point[0], point[1])
            self._points.append(p)

    def make_copy(self) -> L:
        """
        Make a deep copy of self

        Returns:
             The deep copy of self
        """
        new_copy = copy.deepcopy(self)
        return new_copy

    def __eq__(self, other: L) -> bool:
        """
        Check if lines are the same based on their points

        Returns:
            True if lines are the same
        """
        if not isinstance(other, Line):
            return False
        return self._points == other.points


class ColorLine(Line):

    def __init__(self) -> None:
        super().__init__()
        self._color: QColor = QColor.fromRgb(0, 0, 0)  # black

    @property
    def color(self) -> QColor:
        """
        Color of line

        Returns:
             The color
        """
        return self._color

    @color.setter
    def color(self, new_color: QColor) -> None:
        """
        Set the color of line

        Returns:

        """
        assert isinstance(new_color, QColor)
        if new_color.isValid():
            self._color = new_color
        else:
            pass

    def make_copy(self) -> CL:
        """
        Make a deep copy of self

        Returns:
             The deep copy of self
        """
        new_copy = super().make_copy()
        return new_copy

    def __eq__(self, other: CL) -> bool:
        """
        Check color rgb values are the same because
        QColor by default checks if QColors are
        the same instance


        Returns:
            True if color lines are the same
        """
        if super().__eq__(other):
            if self._color.rgb() == other.color.rgb():
                return True
        return False

    def invert_color(self) -> None:
        """
        Invert the color of line for dark mode

        Returns:

        """
        r, g, b = self._color.red(), self._color.green(), self._color.blue()
        self._color = QColor.fromRgb(255 - r, 255 - g, 255 - b)


if __name__ == "__main__":
    pass
