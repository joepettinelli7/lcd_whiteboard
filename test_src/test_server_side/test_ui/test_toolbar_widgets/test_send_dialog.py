from unittest.mock import patch
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import QHBoxLayout
from pytestqt.qtbot import QtBot

from src.server_side.backend.models.recipient_select_model import RecipientSelectModel
from src.server_side.ui.toolbar_widgets.send_dialog import RecipientSelectListView, SendDialog


@pytest.fixture
def rs_lv_fix(qtbot: QtBot) -> RecipientSelectListView:
    lv = RecipientSelectListView()
    qtbot.addWidget(lv)
    return lv


@pytest.fixture
def sd_fix(qtbot: QtBot) -> SendDialog:
    sd = SendDialog()
    qtbot.addWidget(sd)
    return sd


class TestRecipientSelectListView:

    def test_init(self, qtbot: QtBot) -> None:
        """

        """
        with patch('PyQt5.QtCore.QSortFilterProxyModel.sort') as patch_sort:
            list_view = RecipientSelectListView()
            assert isinstance(list_view.model(), QSortFilterProxyModel)
            patch_sort.assert_called_once_with(0, Qt.SortOrder.AscendingOrder)

    @pytest.mark.parametrize('stat_val', [0, 1])
    def test_add_recipient(self, rs_lv_fix: RecipientSelectListView, stat_val: int) -> None:
        """

        """
        with patch.object(rs_lv_fix._cb_model, 'add_recipient') as patch_add:
            patch_add.return_value = stat_val
            return_val = rs_lv_fix.add_recipient('test_name', '111')
            assert return_val == stat_val

    def test_get_checked_numbers(self, rs_lv_fix: RecipientSelectListView) -> None:
        """

        """
        rs_lv_fix.cb_model._checked_recipients = {'test_name1': '111', 'test_name2': '222'}
        numbers = rs_lv_fix.get_checked_numbers()
        assert numbers == ['111', '222']

    def test_cb_model_getter(self, rs_lv_fix: RecipientSelectListView) -> None:
        """

        """
        assert rs_lv_fix._cb_model is rs_lv_fix.cb_model
        assert isinstance(rs_lv_fix.cb_model, RecipientSelectModel)


class TestSendDialog:

    def test_setup_button_layout(self, sd_fix: SendDialog) -> None:
        """

        """
        with patch('PyQt5.QtWidgets.QHBoxLayout.addWidget') as patch_add:
            h_layout = sd_fix.setup_button_layout()
            patch_add.assert_any_call(sd_fix._cancel_button)
            patch_add.assert_any_call(sd_fix._send_button)
            assert isinstance(h_layout, QHBoxLayout)

    def test_recipient_view_getter(self, sd_fix: SendDialog) -> None:
        """

        """
        assert sd_fix._recipient_view is sd_fix.recipient_view
        assert isinstance(sd_fix.recipient_view, RecipientSelectListView)


if __name__ == "__main__":
    pass
