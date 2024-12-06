import pickle
import threading
import time
import typing
from unittest.mock import patch, MagicMock
import socket
import pytest
from PyQt5.QtCore import pyqtBoundSignal

from src.server_side.backend.messaging.ngrok import NgrokClient
from src.server_side.backend.messaging.server import Server, SOCKET_HOST, SOCKET_PORT
from src.server_side.backend.messaging.twilio import TwilioClient


@pytest.fixture
def server_fix() -> Server:
    server = Server()
    server._sock = MagicMock()
    server._should_run = True
    return server


class IntentionalError(RuntimeError):
    pass


class TestServer:

    def test_run1(self, server_fix: Server) -> None:
        """
        Test should_run
        """
        server_fix._should_run = True
        server_fix._sock = None
        with patch.object(socket, 'socket') as patch_sock:
            with patch.object(patch_sock, 'bind') as patch_bind:
                with patch.object(server_fix, 'handle_client_requests') as patch_handle:
                    # Intentionally raise error to break loop because don't use start().
                    # Raise error in last function called
                    patch_handle.side_effect = IntentionalError
                    with pytest.raises(IntentionalError):
                        # server_fix.start()
                        server_fix.run()
                        patch_sock.assert_called_once()
                        patch_bind.assert_called_once_with((SOCKET_HOST, SOCKET_PORT))
                        patch_handle.assert_called()

    @pytest.mark.parametrize('error', [socket.timeout, OSError])
    def test_run2(self, server_fix: Server, error: typing.Any) -> None:
        """
        Test error handling
        """
        with patch.object(server_fix, 'handle_client_requests') as patch_handle:
            patch_handle.side_effect = error

    @pytest.mark.parametrize('data', [b"test_data", None])
    def test_handle_client_requests1(self, server_fix: Server, data: typing.Optional[bytes]) -> None:
        """
        Test received data handling
        """
        with patch.object(server_fix, 'notify_flask_to_start') as patch_notify:
            with patch.object(server_fix._sock, 'accept') as patch_accept:
                mock_client_conn = MagicMock()
                patch_accept.return_value = mock_client_conn, MagicMock()
                with patch.object(mock_client_conn, 'recv') as patch_recv:
                    patch_recv.return_value = data
                    with patch.object(server_fix, 'process_data') as patch_proc:
                        with patch.object(mock_client_conn, 'sendall') as patch_sendall:
                            with patch.object(mock_client_conn, 'close') as patch_close:
                                server_fix.handle_client_requests()
                                patch_notify.assert_called_once()
                                patch_accept.assert_called_once()
                                if data is not None:
                                    patch_proc.assert_called_once_with(data)
                                    patch_sendall.assert_called_once()
                                    patch_close.assert_called_once()
                                else:
                                    patch_proc.assert_not_called()
                                    patch_sendall.assert_not_called()
                                    patch_close.assert_not_called()

    def test_handle_client_requests2(self, server_fix: Server) -> None:
        """
        Test socket timeout
        """
        server_fix._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with pytest.raises(socket.timeout):
            server_fix.handle_client_requests()

    @pytest.mark.parametrize('client_data', [{'start_ngrok': True}, {'name': 'test_name', 'number': '123'}])
    def test_process_data(self, server_fix: Server, client_data: typing.Dict[str, typing.Any]) -> None:
        """

        """
        client_data_bytes: bytes = pickle.dumps(client_data)
        test_ngrok_status = 'test_ngrok_status'
        test_recip_status = 'test_recip_status'
        with patch.object(server_fix, 'process_ngrok_data') as patch_ngrok_process:
            patch_ngrok_process.return_value = test_ngrok_status
            with patch.object(server_fix, 'process_recipient_data') as patch_recip_process:
                patch_recip_process.return_value = test_recip_status
                proc_response: bytes = server_fix.process_data(client_data_bytes)
                proc_response: str = pickle.loads(proc_response)
                if 'start_ngrok' in client_data:
                    assert proc_response == test_ngrok_status
                else:
                    assert proc_response == test_recip_status

    @pytest.mark.parametrize('ngrok_data', [{'start_ngrok': True}, {'start_ngrok': False}])
    def test_process_ngrok_data(self, server_fix: Server, ngrok_data: typing.Dict[str, bool]) -> None:
        """

        """
        with patch.object(server_fix, 'start_ngrok') as patch_start:
            patch_start.return_value = True
            response = server_fix.process_ngrok_data(ngrok_data)
            if ngrok_data['start_ngrok']:
                assert 'Ngrok started: True' in response
            else:
                assert 'invalid' in response

    @pytest.mark.parametrize('url', ['test_url', None])
    def test_start_ngrok1(self, server_fix: Server, url: typing.Optional[str]) -> None:
        """
        Test different url value
        """
        with patch.object(server_fix.ngrok_client, 'set_account_info') as patch_set:
            patch_set.return_value = True
            with patch.object(server_fix.ngrok_client, 'start_ngrok') as patch_client_start:
                patch_client_start.return_value = url
                success = server_fix.start_ngrok()
                patch_set.assert_called()
                patch_client_start.assert_called()
                if patch_client_start.return_value == 'test_url':
                    assert success
                else:
                    assert not success

    @pytest.mark.parametrize('set_success', [True, False])
    def test_start_ngrok2(self, server_fix: Server, set_success: bool) -> None:
        """
        Test different set success value
        """
        with patch.object(server_fix.ngrok_client, 'set_account_info') as patch_set:
            patch_set.return_value = set_success
            with patch.object(server_fix.ngrok_client, 'start_ngrok') as patch_client_start:
                patch_client_start.return_value = 'test_url'
                success = server_fix.start_ngrok()
                patch_set.assert_called()
                if patch_set.return_value:
                    patch_client_start.assert_called()
                    assert success
                else:
                    patch_client_start.assert_not_called()
                    assert not success

    def test_process_recipient_data(self, server_fix: Server) -> None:
        """

        """
        test_recip_data = {'name': 'test_name', 'number': '123'}
        with patch.object(pyqtBoundSignal, 'emit') as patch_emit:
            with patch.object(server_fix, 'wait_for_add') as patch_wait:
                with patch.object(server_fix, 'make_recipient_response') as patch_make:
                    patch_make.return_value = "recipient response"
                    response = server_fix.process_recipient_data(test_recip_data)
                    patch_emit.assert_called_once_with(('test_name', '123'))
                    patch_wait.assert_called_once()
                    patch_make.assert_called_once()
                    assert isinstance(response, str)
                    assert server_fix._recipient_added == -1

    @pytest.mark.parametrize("added_status", [-1, 0])
    def test_wait_for_add(self, server_fix: Server, added_status: int) -> None:
        """

        """
        max_wait = 0.5
        server_fix._recipient_added = added_status
        if server_fix._recipient_added == -1:
            # will reach max time
            test_start_time = time.time()
            server_fix.wait_for_add(max_wait)
            test_end_time = time.time()
            assert test_end_time - test_start_time >= max_wait
        else:
            server_fix.wait_for_add(max_wait)

    @pytest.mark.parametrize("added_status", [-1, 0, 1, 2, 3])
    def test_make_recipient_response(self, server_fix: Server, added_status: int) -> None:
        """

        """
        server_fix._recipient_added = added_status
        if added_status < 3:
            response = server_fix.make_recipient_response()
            if added_status == -1:
                assert "Error" in response
            elif added_status == 0:
                assert "Added successfully" in response
            elif added_status == 1:
                assert "Not added successfully" in response
            else:
                assert "Not added successfully" in response
        else:
            with pytest.raises(AssertionError):
                server_fix.make_recipient_response()

    def test_notify_flask_to_start(self, server_fix: Server) -> None:
        """

        """
        with patch.object(threading.Condition, "notifyAll") as patch_notify:
            server_fix.notify_flask_to_start()
            patch_notify.assert_called_once()

    @pytest.mark.parametrize("test_sock", [MagicMock(), None])
    def test_close_socket(self, server_fix: Server, test_sock: typing.Any) -> None:
        """

        """
        with patch.object(socket, 'close') as patch_close:
            server_fix._sock = test_sock
            server_fix.close_socket()
            if isinstance(server_fix._sock, MagicMock):
                patch_close.assert_called_once()
            else:
                patch_close.assert_not_called()
        assert server_fix._sock is None

    def test_ngrok_client_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix.ngrok_client is server_fix._ngrok_client
        assert isinstance(server_fix.ngrok_client, NgrokClient)

    def test_twilio_client_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix.twilio_client is server_fix._twilio_client
        assert isinstance(server_fix.twilio_client, TwilioClient)

    def test_server_condition_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix.server_condition is server_fix._server_condition
        assert isinstance(server_fix.server_condition, threading.Condition)

    def test_sock_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix._sock is not None
        # Socket set to MagicMock in fixture
        assert server_fix.sock is server_fix._sock

    def test_should_run_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix.should_run is server_fix._should_run
        assert isinstance(server_fix.should_run, bool)

    @pytest.mark.parametrize('new_val', [True, False])
    def test_should_run_setter(self, server_fix: Server, new_val: bool) -> None:
        """

        """
        server_fix.should_run = new_val
        assert server_fix._should_run is new_val

    def test_recipient_added_getter(self, server_fix: Server) -> None:
        """

        """
        assert server_fix.recipient_added is server_fix._recipient_added
        assert isinstance(server_fix.recipient_added, int)

    @pytest.mark.parametrize("status", [-1, 0, 1, 2, 3])
    def test_recipient_added_setter(self, server_fix: Server, status: int) -> None:
        """

        """
        if status == 3:
            with pytest.raises(AssertionError):
                server_fix.recipient_added = status
                assert server_fix._recipient_added is status
        else:
            server_fix.recipient_added = status


if __name__ == "__main__":
    pass
