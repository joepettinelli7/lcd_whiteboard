from unittest.mock import patch
import pytest
import typing
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from src.server_side.backend.lines.line import Line, ColorLine


@pytest.fixture
def line_fix() -> Line:
    return Line()


@pytest.fixture
def color_line_fix() -> ColorLine:
    return ColorLine()


class TestLine:

    def test_points_getter(self, line_fix: Line) -> None:
        """

        """
        assert line_fix._points is line_fix.points
        assert isinstance(line_fix.points, list)

    @pytest.mark.parametrize("points_list", [([QPoint(1, 1), QPoint(2, 2), QPoint(3, 3)]), ([QPoint(1, 1)])])
    def test_make_straight(self, line_fix: Line, points_list: typing.List[QPoint]) -> None:
        """

        """
        line_fix._points = points_list
        if len(points_list) > 2:
            first_point = points_list[0]
            last_point = points_list[-1]
            line_fix.make_straight()
            assert line_fix._points[0] is first_point
            assert line_fix._points[-1] is last_point
        else:
            line_fix.make_straight()
            assert line_fix._points is points_list

    @pytest.mark.parametrize("points_list", [([QPoint(1, 1), QPoint(2, 2)]), ([(1, 1), (2, 2)]), ((1, 1),)])
    def test_add_points(self, line_fix: Line, points_list: typing.Any) -> None:
        """

        """
        original_length = len(line_fix._points)
        num_new_points = len(points_list)
        if isinstance(points_list, list):
            line_fix.add_points(points_list)
            new_length = len(line_fix._points)
            assert new_length == original_length + num_new_points
        else:
            with pytest.raises(AssertionError):
                # Should not be nested tuples
                line_fix.add_points(points_list)

    @pytest.mark.parametrize("point", [QPoint(1, 1), (2, 2)])
    def test_add_point(self, line_fix: Line, point: typing.Union[QPoint, typing.Tuple[int, int]]) -> None:
        """

        """
        original_length = len(line_fix._points)
        line_fix.add_point(point)
        new_length = len(line_fix._points)
        assert new_length == original_length + 1
        # Even tuple should be converted to QPoint
        assert isinstance(line_fix._points[-1], QPoint)

    def test_make_copy(self, line_fix: Line) -> None:
        """

        """
        point = QPoint(1, 1)
        line_fix.add_point(point)
        copy = line_fix.make_copy()
        assert line_fix == copy
        assert line_fix is not copy
        line_fix._points.pop()
        assert line_fix != copy

    def test_equal(self) -> None:
        """

        """
        line1 = Line()
        line2 = Line()
        assert line1 == line2
        line1.add_point(QPoint(1, 1))
        assert line1 != line2
        assert line1 != QPoint(1, 1)


class TestColorLine:

    def test_color_getter(self, color_line_fix: ColorLine) -> None:
        """

        """
        assert color_line_fix._color is color_line_fix.color
        assert isinstance(color_line_fix.color, QColor)

    @pytest.mark.parametrize("new_color", [QColor.fromRgbF(0.0, 1.0, 0.5, 1.0), QColor("invalid")])
    def test_color_setter(self, color_line_fix: ColorLine, new_color: QColor) -> None:
        """
        Same logic as Drawing Surface selected color setter

        """
        color_line_fix.color = new_color
        if new_color == QColor.fromRgbF(0.0, 1.0, 0.5, 1.0):
            assert color_line_fix._color is new_color
        else:
            assert color_line_fix._color is not new_color

    def test_make_copy_points(self, color_line_fix: ColorLine) -> None:
        """
        Check that points are copied correctly

        """
        point = QPoint(1, 1)
        color_line_fix.add_point(point)
        copy = color_line_fix.make_copy()
        assert color_line_fix == copy
        assert color_line_fix is not copy
        color_line_fix._points.pop()
        assert color_line_fix != copy

    def test_make_copy_color(self, color_line_fix: ColorLine) -> None:
        """
        Check that the color is copied correctly

        """
        color_line_fix._color = QColor.fromRgbF(0.0, 1.0, 0.5, 1.0)
        copy = color_line_fix.make_copy()
        assert color_line_fix == copy
        assert color_line_fix is not copy
        color_line_fix.color = QColor.fromRgbF(1.0, 1.0, 0.5, 1.0)
        assert color_line_fix != copy

    def test_equal_color(self) -> None:
        """
        Test equal works based on the line color

        """
        line1 = ColorLine()
        line2 = ColorLine()
        assert line1 == line2
        line1._color = QColor.fromRgbF(1.0, 1.0, 0.5, 1.0)
        assert line1._points == line2._points
        assert line1 != line2

    @pytest.mark.parametrize("super_equal", [True, False])
    def test_equal_super_call(self, super_equal: bool) -> None:
        """
        Test equal works based on super class return

        """
        line1 = ColorLine()
        line2 = ColorLine()
        assert line1 == line2
        with patch('src.server_side.backend.lines.line.Line.__eq__') as super_return:
            super_return.return_value = super_equal
            if super_return.return_value:
                assert line1 == line2
            else:
                assert line1 != line2

    def test_invert_color(self, color_line_fix: ColorLine) -> None:
        """

        """
        color = QColor()
        color.setRed(55)
        color.setGreen(100)
        color.setBlue(255)
        color_line_fix._color = color
        color_line_fix.invert_color()
        assert color_line_fix._color.red() == 200
        assert color_line_fix._color.green() == 155
        assert color_line_fix._color.blue() == 0


if __name__ == '__main__':
    pass
