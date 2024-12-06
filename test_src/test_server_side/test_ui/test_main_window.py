import typing
from unittest.mock import patch, MagicMock
import pytest
from PyQt5.QtGui import QColor, QCloseEvent
from PyQt5.QtWidgets import QDialog
from pytestqt.qtbot import QtBot

from src.server_side.backend.messaging.server import Server
from src.server_side.ui.main_window import WhiteboardMW, IMAGE_PAGE


@pytest.fixture
def mw(qtbot: QtBot) -> WhiteboardMW:
    mw = WhiteboardMW()
    mw._client_controller = MagicMock()
    mw._drawing_surface = MagicMock()
    mw._qr_widget = MagicMock()
    mw._server = Server()
    qtbot.addWidget(mw)
    mw.show()
    qtbot.wait_exposed(mw)
    return mw


class TestWhiteboardMW:

    def test_connect_signals(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw, 'update_color_slot') as patch_update_color_slot:
            with patch.object(mw, 'show_send_dialog_slot') as patch_dial_show_slot:
                with patch.object(mw, 'send_dialog_finished_slot') as patch_dial_finish_slot:
                    with patch.object(mw._drawing_surface, 'undo_line_slot') as patch_undo_line_slot:
                        with patch.object(mw._drawing_surface, 'toggle_dark_slot') as patch_toggle_dark_slot:
                            with patch.object(mw, 'show_qr_slot') as patch_qr_slot:
                                mw.connect_signals()
                                mw._drawing_toolbar._color_combobox.currentIndexChanged.emit(1)
                                patch_update_color_slot.assert_called_once()
                                mw._drawing_toolbar._send_action.trigger()
                                patch_dial_show_slot.assert_called_once()
                                mw._send_dialog.done(0)
                                patch_dial_finish_slot.assert_called_once()
                                mw._drawing_toolbar._undo_line_action.trigger()
                                patch_undo_line_slot.assert_called_once()
                                mw._drawing_toolbar.dark_mode_action.trigger()
                                patch_toggle_dark_slot.assert_called_once()
                                mw._drawing_toolbar._show_qr_action.trigger()
                                patch_qr_slot.assert_called_once()

    def test_set_server(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch('src.server_side.backend.messaging.server.Server.__new__') as patch_new:
            with patch('src.server_side.backend.messaging.twilio.TwilioClient.set_account_info') as patch_set:
                patch_new.return_value = mw._server
                with patch.object(mw, 'stop_all') as patch_stop_all:
                    with patch.object(mw, 'add_recipient_slot') as patch_add_recip_slot:
                        mw.set_server()
                        mw._server.should_stop_signal.emit()
                        patch_stop_all.assert_called_once()
                        mw._server.add_recipient_signal.emit(('test', '123'))
                        patch_add_recip_slot.assert_called_once_with(('test', '123'))
                        patch_set.assert_called_once()

    def test_show_mw(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw, 'show') as patch_show:
            with patch.object(mw._drawing_surface, 'setGeometry') as patch_set_geom:
                mw.show_mw()
                patch_show.assert_called_once()
                mw_geom = mw.geometry()
                patch_set_geom.assert_called_once_with(mw_geom)

    @pytest.mark.parametrize('server_success', [True, False])
    def test_start_all(self, mw: WhiteboardMW, server_success: bool) -> None:
        """

        """
        with patch.object(mw, 'start_server') as patch_start_server:
            with patch.object(mw._client_controller, 'start_client') as patch_start_client:
                mw.start_all(server_success)
                if server_success:
                    patch_start_server.assert_called_once()
                    patch_start_client.assert_called_once()
                else:
                    patch_start_server.assert_not_called()
                    patch_start_client.assert_not_called()

    def test_start_server(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw._server, 'start') as patch_start:
            mw.start_server()
            patch_start.assert_called_once()

    def test_update_color_slot(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw._drawing_toolbar._color_combobox, 'get_color') as patch_get:
            patch_get.return_value = QColor('black')
            mw.update_color_slot()
            assert mw._drawing_surface.selected_color == patch_get.return_value

    def test_show_send_dialog_slot(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw._send_dialog, 'open') as patch_open:
            mw.show_send_dialog_slot()
            patch_open.assert_called_once()

    @pytest.mark.parametrize('result', [QDialog.DialogCode.Accepted, 'not_accepted'])
    def test_send_dialog_finished_slot(self, mw: WhiteboardMW, result: typing.Any) -> None:
        """

        """
        with patch.object(mw._send_dialog.recipient_view, 'get_checked_numbers') as patch_get:
            with patch.object(mw, 'send_whiteboard') as patch_send:
                mw.send_dialog_finished_slot(result)
                if result == QDialog.DialogCode.Accepted:
                    patch_get.assert_called_once()
                    patch_send.assert_called_once_with(patch_get.return_value)
                else:
                    patch_get.assert_not_called()
                    patch_send.assert_not_called()

    @pytest.mark.parametrize("save_success", [True, False])
    def test_send_whiteboard(self, mw: WhiteboardMW, save_success: bool) -> None:
        """

        """
        with patch.object(mw._drawing_surface, 'save_whiteboard_image') as patch_save:
            with patch.object(mw._server.twilio_client, 'send_to_all') as patch_send:
                patch_save.return_value = save_success
                mw.send_whiteboard(['111', '222'])
                patch_save.assert_called_once()
                if patch_save.return_value:
                    patch_send.assert_called_once_with(IMAGE_PAGE, ['111', '222'])
                else:
                    patch_send.assert_not_called()

    def test_add_recipient_slot(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw._send_dialog.recipient_view, 'add_recipient') as patch_add:
            patch_add.return_value = 0
            test_recip_info = ('test_name', '111')
            mw.add_recipient_slot(test_recip_info)
            patch_add.assert_called_once_with(test_recip_info[0], test_recip_info[1])
            assert mw._server.recipient_added != -1

    @pytest.mark.parametrize('connected_already', [True, False])
    def test_show_qr_slot(self, mw: WhiteboardMW, connected_already: bool) -> None:
        """

        """
        mw._server.ngrok_client._connected_already = connected_already
        mw._server.ngrok_client._public_url = 'test_url'
        with patch.object(mw._qr_widget, 'set_qr_code') as patch_set:
            with patch.object(mw._qr_widget, 'show') as patch_show:
                with patch.object(mw, 'show_message') as patch_show_message:
                    mw.show_qr_slot()
                    if connected_already:
                        patch_set.assert_called_once()
                        patch_show.assert_called_once()
                        patch_show_message.assert_not_called()
                    else:
                        patch_set.assert_not_called()
                        patch_show.assert_not_called()
                        patch_show_message.assert_called_once()

    def test_show_message(self, mw: WhiteboardMW, qtbot: QtBot) -> None:
        """

        """
        test_message = 'test message'
        with patch('PyQt5.QtWidgets.QMessageBox.setText') as patch_set:
            with patch('PyQt5.QtWidgets.QMessageBox.exec_') as patch_exec:
                mw.show_message(test_message)
                patch_set.assert_called_once_with(test_message)
                patch_exec.assert_called_once()

    def test_closeEvent(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw, 'stop_all') as patch_stop:
            close_event = QCloseEvent()
            mw.closeEvent(close_event)
            patch_stop.assert_called_once()

    def test_stop_all(self, mw: WhiteboardMW) -> None:
        """

        """
        with patch.object(mw._server.ngrok_client, 'disconnect_server') as patch_dis_server:
            with patch.object(mw._client_controller, 'stop_client') as patch_stop_client:
                with patch.object(mw._server, 'wait') as patch_wait:
                    with patch.object(mw._server, 'close_socket') as patch_close_sock:
                        with patch.object(mw._drawing_surface, 'delete_wb_image') as patch_delete:
                            with patch.object(mw._drawing_surface, 'save_config') as patch_save:
                                mw.stop_all()
                                patch_dis_server.assert_called_once()
                                patch_stop_client.assert_called_once()
                                patch_wait.assert_called_once()
                                patch_close_sock.assert_called_once()
                                patch_delete.assert_called_once()
                                patch_save.assert_called_once()


if __name__ == '__main__':
    pass
