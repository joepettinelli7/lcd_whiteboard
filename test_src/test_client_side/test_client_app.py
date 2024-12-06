import pickle
from unittest.mock import patch, MagicMock
import pytest

from src.client_side.client_app import ClientApp, FLASK_PORT, client_process_target


@pytest.fixture
def client_app_fix() -> ClientApp:
    client_app = ClientApp()
    client_app.testing = True
    return client_app


class TestClientApp:

    def test_start_client_app(self, client_app_fix: ClientApp) -> None:
        """

        """
        with patch.object(client_app_fix, 'set_routes') as patch_set:
            with patch.object(client_app_fix, 'server_start_ngrok') as patch_start_serv:
                with patch.object(client_app_fix, 'run') as patch_run:
                    client_app_fix.start_client_app()
                    patch_set.assert_called_once()
                    patch_start_serv.assert_called_once()
                    patch_run.assert_called_once_with(port=FLASK_PORT, debug=False)

    def test_set_routes(self, client_app_fix: ClientApp) -> None:
        """

        """
        with patch.object(client_app_fix, 'add_url_rule') as patch_add:
            client_app_fix.set_routes()
            assert patch_add.call_count == 3

    def test_server_start_ngrok(self, client_app_fix: ClientApp) -> None:
        """

        """
        with patch.object(client_app_fix, 'send_recv') as patch_send_recv:
            client_app_fix.server_start_ngrok()
            patch_send_recv.assert_called_once_with({'start_ngrok': True})

    def test_index(self, client_app_fix: ClientApp) -> None:
        """

        """
        pass

    def test_submit(self, client_app_fix: ClientApp) -> None:
        """

        """
        pass

    def test_serve_image(self, client_app_fix: ClientApp) -> None:
        """

        """
        pass

    def test_send_recv1(self, client_app_fix: ClientApp) -> None:
        """
        Test send recv works without error
        """
        message = {'name': 'test_name', 'number': '123'}
        with patch('socket.socket') as patch_sock:
            patch_sock.return_value = MagicMock()
            with patch.object(patch_sock.return_value, 'recv') as patch_recv:
                patch_recv.return_value = pickle.dumps('server_response')
                server_resp = client_app_fix.send_recv(message)
                assert server_resp == 'server_response'

    def test_send_recv2(self, client_app_fix: ClientApp) -> None:
        """
        Test send recv works with error
        """
        message = {'name': 'test_name', 'number': '123'}
        with patch('socket.socket') as patch_sock:
            patch_sock.return_value = MagicMock()
            with patch.object(patch_sock.return_value, 'recv') as patch_recv:
                patch_recv.side_effect = ConnectionRefusedError
                server_resp = client_app_fix.send_recv(message)
                assert server_resp is None


def test_client_process_target() -> None:
    """

    """
    with patch.object(ClientApp, '__new__') as patch_new:
        patch_new.return_value = MagicMock()
        with patch.object(patch_new.return_value, 'start_client_app') as patch_start:
            client_process_target()
            patch_new.assert_called_once()
            patch_start.assert_called_once()


if __name__ == "__main__":
    pass
