from unittest.mock import patch
import pytest
from PyQt5.QtWidgets import QAction
from pytestqt.qtbot import QtBot

from src.server_side.ui.toolbar_widgets.drawing_toolbar import DrawingToolBar, ColorSelectCb


@pytest.fixture
def tb_fix(qtbot: QtBot) -> DrawingToolBar:
    drawing_toolbar = DrawingToolBar()
    qtbot.addWidget(drawing_toolbar)
    return drawing_toolbar


class TestDrawingToolBar:

    def test_make_send_action(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch.object(tb_fix, 'load_send_icon') as patch_load:
            with patch('PyQt5.QtWidgets.QAction.__new__') as patch_new:
                with patch.object(patch_new.return_value, 'setIconVisibleInMenu') as patch_set:
                    _ = tb_fix.make_send_action()
                    patch_load.assert_called_once()
                    patch_new.assert_called_once()
                    patch_set.assert_called_once_with(True)

    def test_make_undo_action(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch.object(tb_fix, 'load_undo_icon') as patch_load:
            with patch('PyQt5.QtWidgets.QAction.__new__') as patch_new:
                with patch.object(patch_new.return_value, 'setIconVisibleInMenu') as patch_set:
                    _ = tb_fix.make_undo_action()
                    patch_load.assert_called_once()
                    patch_new.assert_called_once()
                    patch_set.assert_called_once_with(True)

    def test_make_qr_action(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch.object(tb_fix, 'load_qr_icon') as patch_load:
            with patch('PyQt5.QtWidgets.QAction.__new__') as patch_new:
                with patch.object(patch_new.return_value, 'setIconVisibleInMenu') as patch_set:
                    _ = tb_fix.make_qr_action()
                    patch_load.assert_called_once()
                    patch_new.assert_called_once()
                    patch_set.assert_called_once_with(True)

    def test_make_dark_mode_action(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch.object(tb_fix, 'load_dark_mode_icon') as patch_load:
            with patch('PyQt5.QtWidgets.QAction.__new__') as patch_new:
                with patch.object(patch_new.return_value, 'setIconVisibleInMenu') as patch_set:
                    _ = tb_fix.make_dark_mode_action()
                    patch_load.assert_called_once()
                    patch_new.assert_called_once()
                    patch_set.assert_called_once_with(True)

    def test_load_send_icon(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch('PyQt5.QtGui.QIcon.__new__') as patch_new:
            tb_fix.load_send_icon()
            patch_new.assert_called_once()

    def test_load_undo_icon(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch('PyQt5.QtGui.QIcon.__new__') as patch_new:
            tb_fix.load_undo_icon()
            patch_new.assert_called_once()

    def test_load_qr_icon(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch('PyQt5.QtGui.QIcon.__new__') as patch_new:
            tb_fix.load_qr_icon()
            patch_new.assert_called_once()

    def test_load_dark_mode_icon(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        with patch('PyQt5.QtGui.QIcon.__new__') as patch_new:
            tb_fix.load_dark_mode_icon()
            patch_new.assert_called_once()

    def test_color_combobox_getter(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        assert tb_fix._color_combobox is tb_fix.color_combobox
        assert isinstance(tb_fix.color_combobox, ColorSelectCb)

    def test_send_action_getter(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        assert tb_fix._send_action is tb_fix.send_action
        assert isinstance(tb_fix.send_action, QAction)

    def test_undo_line_action_getter(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        assert tb_fix._undo_line_action is tb_fix.undo_line_action
        assert isinstance(tb_fix.undo_line_action, QAction)

    def test_show_qr_action_getter(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        assert tb_fix._show_qr_action is tb_fix.show_qr_action
        assert isinstance(tb_fix.show_qr_action, QAction)

    def test_dark_mode_action_getter(self, tb_fix: DrawingToolBar) -> None:
        """

        """
        assert tb_fix._dark_mode_action is tb_fix.dark_mode_action
        assert isinstance(tb_fix.dark_mode_action, QAction)


if __name__ == "__main__":
    pass
