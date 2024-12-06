import io
import subprocess
import urllib.error
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock
import pytest
from pyngrok import ngrok, conf
from pyngrok.exception import PyngrokNgrokError

from src.server_side.backend.messaging.ngrok import NgrokClient
from src.server_side.backend.messaging.ngrok import FLASK_PORT


@pytest.fixture
def ngrok_fix() -> NgrokClient:
    ngrok_client = NgrokClient()
    return ngrok_client


@pytest.fixture
def info_fix() -> Dict[str, str]:
    test_info = {'twilio_account_sid': 'aaa',
                 'twilio_auth_token': 'bbb',
                 'twilio_number': '+123',
                 'ngrok_auth_token': 'ccc'}
    return test_info


class TestNgrokClient:

    @pytest.mark.parametrize('conn', [True, False])
    def test_start_ngrok(self, ngrok_fix: NgrokClient, conn: bool) -> None:
        """

        """
        with patch.object(ngrok_fix, "connect_server") as patch_conn:
            assert not ngrok_fix._connected_already
            patch_conn.return_value = conn
            _ = ngrok_fix.start_ngrok()
            patch_conn.assert_called_once_with(FLASK_PORT)
            if patch_conn.return_value:
                assert ngrok_fix._connected_already
            else:
                assert not ngrok_fix._connected_already

    @pytest.mark.parametrize('info_exists', [True, False])
    def test_set_account_info(self, ngrok_fix: NgrokClient, info_fix: Dict[str, str], info_exists: bool) -> None:
        """
        This file is purposely not available because it
        contains ngrok and twilio account credentials
        """
        with patch("pickle.load") as patch_load:
            with patch("builtins.open") as patch_open:
                # Set return value and side effect before calling
                if info_exists:
                    patch_load.return_value = info_fix
                else:
                    patch_open.side_effect = FileNotFoundError
                is_set = ngrok_fix.set_account_info()
                if isinstance(patch_load.return_value, dict):
                    # The info fix got returned
                    assert is_set
                    assert ngrok_fix._auth_token == info_fix['ngrok_auth_token']
                else:
                    # The error is raised
                    assert isinstance(patch_load.return_value, MagicMock)
                    assert not is_set
                    assert ngrok_fix._auth_token is None

    def test_connect_server1(self, ngrok_fix: NgrokClient, info_fix: Dict[str, str]) -> None:
        """
        Test successful flow
        """
        with patch.object(conf, 'get_default') as patch_get_conf:
            with patch.object(ngrok, 'connect') as patch_connect:
                ngrok_fix._auth_token = info_fix['ngrok_auth_token']
                mock_config = MagicMock()
                patch_get_conf.return_value = mock_config
                mock_tunnel = MagicMock()
                mock_tunnel.public_url = "test_url"
                patch_connect.return_value = mock_tunnel
                success = ngrok_fix.connect_server(FLASK_PORT)
                patch_get_conf.assert_called_once()
                assert mock_config.auth_token == info_fix['ngrok_auth_token']
                patch_connect.assert_called_once_with(FLASK_PORT)
                assert ngrok_fix._public_url == "test_url"
                assert success

    @pytest.mark.parametrize('error', [OSError, AssertionError,
                                       urllib.error.HTTPError('url', 1, 'msg', 'hdrs', io.BytesIO(b'')),
                                       PyngrokNgrokError('test')])
    def test_connect_server2(self, ngrok_fix: NgrokClient, error: Any) -> None:
        """
        Test all known errors caught
        """
        with patch.object(conf, 'get_default'):
            with patch.object(ngrok, 'connect') as patch_connect:
                patch_connect.side_effect = error
                success = ngrok_fix.connect_server(FLASK_PORT)
                patch_connect.assert_called_once_with(FLASK_PORT)
                assert not success

    @pytest.mark.parametrize('connected', [True, False])
    def test_disconnect_server(self, ngrok_fix: NgrokClient, connected: bool) -> None:
        """

        """
        ngrok_fix._public_url = 'test_url'
        with patch.object(ngrok, 'disconnect') as patch_disc:
            with patch.object(ngrok, 'get_tunnels') as patch_get_tun:
                with patch.object(ngrok, 'kill') as patch_kill:
                    ngrok_fix._connected_already = connected
                    ngrok_fix.disconnect_server()
                    if connected:
                        patch_disc.assert_called_once_with("test_url")
                        patch_get_tun.assert_called_once()
                        patch_kill.assert_called_once()
                    else:
                        patch_disc.assert_not_called()
                        patch_get_tun.assert_not_called()
                        patch_kill.assert_not_called()
                    assert not ngrok_fix._connected_already

    # @pytest.mark.parametrize('pid', [123, None])
    # def test_ensure_disconnect(self, ngrok_fix: NgrokClient, pid: bool) -> None:
    #     """
    #
    #     """
    #     with patch.object(subprocess, 'run') as patch_run:
    #         with patch.object(ngrok_fix, 'get_pid') as patch_pid:
    #             patch_pid.return_value = pid
    #             ngrok_fix.ensure_disconnect()
    #             patch_pid.assert_called_once()
    #             if pid:
    #                 patch_run.assert_any_call(['kill', '-9', pid])
    #             patch_run.assert_any_call(['ps', 'aux'], capture_output=True, text=True)

    # @pytest.mark.parametrize('lines', [["ngrok 123"], ["ngrok 123 grep"]])
    # def test_get_pid(self, ngrok_fix: NgrokClient, lines: List[str]) -> None:
    #     """
    #
    #     """
    #     pid = ngrok_fix.get_pid(lines)
    #     if lines == ["ngrok 123"]:
    #         assert pid == "123"
    #     else:
    #         assert pid is None

    def test_public_url_getter(self, ngrok_fix: NgrokClient) -> None:
        """

        """
        ngrok_fix._public_url = 'python.org'
        assert ngrok_fix._public_url is ngrok_fix.public_url

    def test_connected_already_getter(self, ngrok_fix: NgrokClient) -> None:
        """

        """
        assert ngrok_fix._connected_already is ngrok_fix.connected_already
        assert isinstance(ngrok_fix.connected_already, bool)


if __name__ == "__main__":
    pass
