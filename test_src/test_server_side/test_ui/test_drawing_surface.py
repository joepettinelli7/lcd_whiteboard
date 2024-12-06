from unittest.mock import patch
import pytest
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt, QLine, QRect
from PyQt5.QtGui import QColor, QPixmap, QPainter
from pytestqt.qtbot import QtBot

from src.server_side.backend.configs.drawing_surface_config import DARK_KEY
from src.server_side.backend.lines.line import ColorLine
from src.server_side.backend.lines.line_list import LineList
from src.server_side.ui.drawing_surface import DrawingSurface
from src.server_side.ui.drawing_surface import IMAGE_PATH, IMAGE_NAME


@pytest.fixture
def ds(qtbot: QtBot) -> DrawingSurface:
    ds = DrawingSurface()
    qtbot.addWidget(ds)
    ds.show()
    qtbot.wait_exposed(ds)
    return ds


@pytest.fixture
def line_list_fix() -> LineList:
    points_list = [[QPoint(1, 1), QPoint(2, 2), QPoint(3, 3)], [QPoint(1, 1)]]
    line_list = LineList()
    for points in points_list:
        color_line = ColorLine()
        color_line.add_points(points)
        line_list.add_line(color_line)
    return line_list


class TestDrawingSurface:

    @pytest.mark.parametrize("button", [Qt.LeftButton, Qt.RightButton])
    def test_mouse_press_event(self, ds: DrawingSurface, qtbot: QtBot, button: Qt.MouseButton) -> None:
        """

        """
        p = QPoint()
        with patch('PyQt5.QtGui.QMouseEvent.pos', return_value=p) as mock_pos:
            qtbot.mousePress(ds, button)
            if button == Qt.LeftButton:
                assert p == ds._current_line.points[-1]
                assert ds._current_line.color is ds._selected_color
            else:
                mock_pos.assert_not_called()
                assert len(ds._current_line.points) == 0

    @pytest.mark.parametrize("button", [Qt.LeftButton, Qt.RightButton])
    def test_mouse_release_event_1(self, ds: DrawingSurface, qtbot: QtBot, button: Qt.MouseButton) -> None:
        """
        Test the correct behavior when left or right mouse button clicked
        """
        initial_num_lines = len(ds._all_lines.line_list)
        points = [QPoint(1, 1), QPoint(2, 2)]
        ds._current_line.add_points(points)
        qtbot.mouseRelease(ds, button)
        if button == Qt.LeftButton:
            final_num_lines = len(ds._all_lines.line_list)
            assert final_num_lines == initial_num_lines + 1
            assert points == ds._all_lines.line_list[-1].points
        else:
            final_num_lines = len(ds._all_lines.line_list)
            assert final_num_lines == initial_num_lines

    @pytest.mark.parametrize("mock_points_list", [[QPoint(1, 1), QPoint(1, 2)], []])
    def test_mouse_release_event_2(self, ds: DrawingSurface, qtbot: QtBot, mock_points_list) -> None:
        """
        Test the correct behavior with different list lengths
        """
        initial_num_lines = len(ds._all_lines.line_list)
        ds._current_line.add_points(mock_points_list)
        if len(ds._current_line.points) > 0:
            qtbot.mouseRelease(ds, Qt.LeftButton)
            final_num_lines = len(ds._all_lines.line_list)
            assert final_num_lines == initial_num_lines + 1
            assert mock_points_list == ds._all_lines.line_list[-1].points
            assert len(ds._current_line.points) == 0
        else:
            with patch('src.server_side.ui.drawing_surface.DrawingSurface.handle_no_points_error') as mock_handle:
                qtbot.mouseRelease(ds, Qt.LeftButton)
                mock_handle.assert_called_once()
                final_num_lines = len(ds._all_lines.line_list)
                assert final_num_lines == initial_num_lines

    @pytest.mark.parametrize("button", [Qt.LeftButton, Qt.RightButton])
    def test_mouse_move_event(self, ds: DrawingSurface, qtbot: QtBot, button: Qt.MouseButton) -> None:
        """

        """
        pass

    def test_paint_event1(self, ds: DrawingSurface, qtbot: QtBot, line_list_fix: LineList) -> None:
        """
        Test with points in line
        """
        ds._current_line.add_points([QPoint(1, 1), QPoint(2, 2)])
        ds._all_lines = line_list_fix
        num_old_lines = len(ds._all_lines.line_list)
        total_lines = 1 + num_old_lines
        with patch.object(ds, 'paint_line') as patch_paint_line:
            with patch('PyQt5.QtWidgets.QWidget.update') as patch_update:
                ds.repaint()
                assert patch_paint_line.call_count == total_lines
                patch_update.assert_called_once()

    def test_paint_event2(self, ds: DrawingSurface, qtbot: QtBot, line_list_fix: LineList) -> None:
        """
        Test handle error
        """
        with patch.object(ds, 'paint_line') as patch_paint_line:
            patch_paint_line.side_effect = AssertionError
            with patch.object(ds, 'handle_no_points_error') as patch_handle:
                with patch('PyQt5.QtWidgets.QWidget.update') as patch_update:
                    ds.repaint()
                    patch_handle.assert_called_once()
                    patch_update.assert_called_once()

    @pytest.mark.parametrize("test_points", [[], [QPoint(1, 1)], [QPoint(1, 1), QPoint(2, 2)]])
    def test_paint_line(self, ds: DrawingSurface, qtbot: QtBot, line_list_fix: LineList,
                        test_points: typing.List[QPoint]) -> None:
        """

        """
        test_line = ColorLine()
        test_line.add_points(test_points)
        with patch('PyQt5.QtGui.QPainter.drawPoint') as patch_draw_point:
            with patch.object(ds, 'line_generator') as patch_generator:
                if len(test_line.points) == 2:
                    patch_generator.return_value = [QLine(test_line.points[0], test_line.points[1])]
                with patch('PyQt5.QtGui.QPainter.drawLine') as patch_draw_line:
                    painter = QPainter(ds)
                    ds.paint_line(test_line, painter)
                    if len(test_line.points) == 0:
                        patch_draw_point.assert_not_called()
                        patch_draw_line.assert_not_called()
                    elif len(test_line.points) == 1:
                        patch_draw_point.assert_called_with(test_line.points[0])
                    else:
                        patch_generator.assert_called_once_with(test_line.points)
                        patch_draw_line.assert_called_once_with(patch_generator.return_value[0])
                    painter.end()

    @pytest.mark.parametrize("points", [[QPoint(1, 1), QPoint(2, 2), QPoint(3, 3)], [QPoint()]])
    def test_line_generator(self, points: typing.List[QPoint]) -> None:
        """

        """
        ds = DrawingSurface
        if len(points) == 1:
            with pytest.raises(AssertionError):
                for _ in ds.line_generator(points):
                    pass
        else:
            i = 0
            for line in ds.line_generator(points):
                assert isinstance(line, QtCore.QLine)
                assert line == QLine(points[i], points[i + 1])
                i += 1

    @staticmethod
    def test_handle_no_points_error() -> None:
        """

        """
        ds = DrawingSurface
        ds.handle_no_points_error()

    @pytest.mark.parametrize(['success', 'exists'], [(True, True), (False, False)])
    def test_save_whiteboard_image(self, ds: DrawingSurface, success: bool, exists: bool) -> None:
        """
        success and exists are independent
        """
        with patch.object(ds, 'get_whiteboard_pixmap') as patch_get_pixmap:
            with patch('PyQt5.QtGui.QPixmap.save') as patch_save_pixmap:
                with patch('os.mkdir') as patch_mkdir:
                    with patch('os.path.exists') as patch_exists:
                        patch_exists.return_value = exists
                        patch_get_pixmap.return_value = QPixmap()
                        patch_save_pixmap.return_value = success
                        got_pixmap = ds.save_whiteboard_image()
                        if not patch_exists.return_value:
                            patch_mkdir.assert_called_once_with(IMAGE_PATH)
                        else:
                            patch_mkdir.assert_not_called()
                        patch_save_pixmap.assert_called_once_with(IMAGE_PATH + IMAGE_NAME, "PNG")
                        assert got_pixmap == success

    def test_get_whiteboard_pixmap(self, ds: DrawingSurface) -> None:
        """

        """
        with patch('PyQt5.QtWidgets.QFrame.rect') as patch_rect:
            with patch('PyQt5.QtWidgets.QFrame.grab') as patch_grab:
                patch_rect.return_value = QRect()
                patch_grab.return_value = QPixmap()
                pixmap = ds.get_whiteboard_pixmap()
                patch_rect.assert_called_once()
                patch_grab.assert_called_once_with(patch_rect.return_value)
                assert pixmap == patch_grab.return_value

    @pytest.mark.parametrize('exists', [True, False])
    def test_delete_wb_image(self, ds: DrawingSurface, exists: bool) -> None:
        """

        """
        with patch('os.path.exists') as patch_exist:
            with patch('os.remove') as patch_remove:
                patch_exist.return_value = exists
                ds.delete_wb_image()
                if patch_exist.return_value:
                    patch_remove.assert_called_once_with(IMAGE_PATH + IMAGE_NAME)
                else:
                    patch_remove.assert_not_called()

    @pytest.mark.parametrize("line", [ColorLine(), None])
    def test_undo_line_slot(self, ds: DrawingSurface, line: typing.List[ColorLine]) -> None:
        """

        """
        if isinstance(line, ColorLine):
            ds._all_lines._line_list.append(line)
        orig_line_length = len(ds._all_lines._line_list)
        with patch('PyQt5.QtWidgets.QWidget.update') as patch_update:
            ds.undo_line_slot()
            new_line_length = len(ds._all_lines._line_list)
            if line:
                # Line length will be 1
                patch_update.assert_called_once()
                assert new_line_length == orig_line_length - 1
            else:
                patch_update.assert_not_called()
                assert new_line_length == orig_line_length

    @pytest.mark.parametrize("dark", [True, False])
    def test_toggle_dark_slot(self, ds: DrawingSurface, dark: bool) -> None:
        """

        """
        ds._config[DARK_KEY] = dark
        new_color = "white" if dark else "black"
        with patch.object(ds._all_lines, 'invert_lines_colors') as patch_invert:
            with patch('PyQt5.QtWidgets.QFrame.update') as patch_update:
                with patch('PyQt5.QtWidgets.QFrame.setStyleSheet') as patch_set:
                    orig_mode = ds._config[DARK_KEY]
                    ds.toggle_dark_slot()
                    patch_invert.assert_called_once()
                    patch_update.assert_called_once()
                    patch_set.assert_called_once_with(f"background-color: {new_color};")
                    new_mode = ds._config[DARK_KEY]
                    assert orig_mode != new_mode

    @pytest.mark.parametrize("dark", [True, False])
    def test_apply_config(self, ds: DrawingSurface, dark: bool) -> None:
        """

        """
        ds._config[DARK_KEY] = dark
        color = "black" if dark else "white"
        with patch('PyQt5.QtWidgets.QFrame.update') as patch_update:
            with patch('PyQt5.QtWidgets.QFrame.setStyleSheet') as patch_set:
                ds.apply_config()
                patch_update.assert_called_once()
                patch_set.assert_called_once_with(f"background-color: {color};")

    def test_save_config(self, ds: DrawingSurface) -> None:
        """

        """
        with patch.object(ds._config, 'save') as patch_save:
            ds.save_config()
            patch_save.assert_called_once()

    def test_center_getter(self, ds: DrawingSurface) -> None:
        """

        """
        # left, top, width, height
        with patch('PyQt5.QtWidgets.QWidget.geometry', return_value=QtCore.QRect(10, 20, 400, 401)):
            assert ds.center == QPoint(210, 220)

    def test_selected_color_getter(self, ds: DrawingSurface) -> None:
        """

        """
        assert ds.selected_color is ds._selected_color
        assert isinstance(ds.selected_color, QColor)

    @pytest.mark.parametrize("new_color", [QColor('black'), QColor('red'), QColor('invalid')])
    def test_selected_color_setter(self, ds: DrawingSurface, new_color: QColor) -> None:
        """

        """
        ds.selected_color = new_color
        if new_color == QColor('invalid'):
            assert ds._selected_color is not new_color
        else:
            assert ds._selected_color is new_color


if __name__ == '__main__':
    pass
