import pytest

import typing

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from src.server_side.backend.lines.line import ColorLine
from src.server_side.backend.lines.line_list import LineList


@pytest.fixture
def line_list_fix() -> LineList:
    line_list = LineList()
    color_line1 = ColorLine()
    color_line1.add_point(QPoint(1, 1))
    color_line2 = ColorLine()
    color_line2.add_point(QPoint(2, 2))
    line_list.add_line(color_line1)
    line_list.add_line(color_line2)
    return line_list


class TestLineList:

    def test_line_list_getter(self, line_list_fix: LineList) -> None:
        """

        """
        assert line_list_fix._line_list is line_list_fix.line_list
        assert isinstance(line_list_fix.line_list, list)

    def test_get_colors(self, line_list_fix: LineList) -> None:
        """

        """
        num_lines = len(line_list_fix._line_list)
        colors = line_list_fix.get_colors()
        num_colors = len(colors)
        assert num_lines == num_colors
        for color in colors:
            assert isinstance(color, QColor)

    @pytest.mark.parametrize("points", [[QPoint()], []])
    def test_add_line(self, line_list_fix: LineList, points: typing.List[QPoint]) -> None:
        """

        """
        original_num_lines = len(line_list_fix._line_list)
        color_line = ColorLine()
        color_line.add_points(points)
        line_list_fix.add_line(color_line)
        new_num_lines = len(line_list_fix._line_list)
        if len(points) == 1:
            assert new_num_lines == original_num_lines + 1
        else:
            # Line not added if no points
            assert len(points) == 0
            assert new_num_lines == original_num_lines

    def test_remove_last_line(self, line_list_fix: LineList) -> None:
        """

        """
        original_num_lines = len(line_list_fix._line_list)
        last_line = line_list_fix._line_list[-1]
        line_list_fix.remove_last_line()
        new_num_lines = len(line_list_fix._line_list)
        assert new_num_lines == original_num_lines - 1
        assert last_line not in line_list_fix._line_list
        # Make sure IndexError handled
        line_list_fix._line_list.clear()
        line_list_fix.remove_last_line()

    def test_invert_lines_colors(self, line_list_fix: LineList) -> None:
        """

        """
        line_list_fix.invert_lines_colors()
        for line in line_list_fix._line_list:
            # Lines were black before invert
            assert line._color.red() == 255
            assert line._color.green() == 255
            assert line._color.blue() == 255


if __name__ == "__main__":
    pass
