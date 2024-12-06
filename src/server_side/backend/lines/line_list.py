import typing

from PyQt5.QtGui import QColor

from src.server_side.backend.lines.line import ColorLine


class LineList:

    def __init__(self) -> None:
        super().__init__()
        self._line_list: typing.List[ColorLine] = []

    @property
    def line_list(self) -> typing.List[ColorLine]:
        """
        The list of all lines to be painted on drawing surface

        Returns:
             The list of all lines
        """
        return self._line_list

    def get_colors(self) -> typing.List[QColor]:
        """
        Get colors used for all lines

        Returns:
             List of all colors
        """
        colors = [color_line.color for color_line in self._line_list]
        return colors

    def add_line(self, color_line: ColorLine) -> None:
        """
        Add a color line to the list of lines

        Args:
            color_line: The line to add

        Returns:

        """
        if len(color_line.points) > 0:
            self._line_list.append(color_line)
        else:
            pass

    def remove_last_line(self) -> None:
        """
        Remove the last line in list.
        Called when user click undo

        Returns:

        """
        try:
            self._line_list.pop()
        except IndexError:
            pass

    def invert_lines_colors(self) -> None:
        """
        Invert the color of the lines for dark mode

        Returns:

        """
        for color_line in self._line_list:
            color_line.invert_color()


if __name__ == "__main__":
    pass
