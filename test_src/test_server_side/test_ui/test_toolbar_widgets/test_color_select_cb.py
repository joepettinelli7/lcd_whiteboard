from unittest.mock import patch
import pytest
from PyQt5.QtGui import QColor
from pytestqt.qtbot import QtBot

from src.server_side.backend.models.color_select_model import ColorSelectModel
from src.server_side.ui.toolbar_widgets.color_select_cb import ColorSelectCb


@pytest.fixture
def cb_fix(qtbot: QtBot) -> ColorSelectCb:
    cb = ColorSelectCb()
    qtbot.addWidget(cb)
    return cb


class TestColorSelectCb:

    @pytest.mark.parametrize('index', [1, 2, 3])
    def test_get_color(self, cb_fix: ColorSelectCb, index: int) -> None:
        with patch('PyQt5.QtWidgets.QComboBox.currentIndex') as patch_idx:
            patch_idx.return_value = index
            color = cb_fix.get_color()
            patch_idx.assert_called_once()
            if index == 1:
                assert color == QColor('red')
            elif index == 2:
                assert color == QColor('orange')
            else:
                assert color == QColor('yellow')

    def test_cb_model_getter(self, cb_fix: ColorSelectCb) -> None:
        assert cb_fix._cb_model is cb_fix.cb_model
        assert isinstance(cb_fix.cb_model, ColorSelectModel)


if __name__ == "__main__":
    pass
