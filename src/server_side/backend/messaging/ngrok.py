# https://ngrok.github.io/ngrok-python/

import os
import pickle
import traceback
import typing
import urllib.error
from pyngrok import conf, ngrok
from pyngrok.exception import PyngrokNgrokError

from src.server_side.app import ROOT_DIR

FLASK_PORT = 6000
NGROK_INFO_PATH: str = os.path.join(ROOT_DIR, 'src', 'server_side', 'backend', 'configs', 'wb_accounts_config.pkl')


class NgrokClient:
    """
    ngrok client to establish tunnel to ngrok server
    and also assign public URL for client app

    """

    def __init__(self) -> None:
        super().__init__()
        self._auth_token: typing.Optional[str] = None
        self._public_url: typing.Optional[str] = None
        self._connected_already: bool = False

    def start_ngrok(self) -> typing.Optional[str]:
        """
        Start the ngrok client and tunnel

        Returns:
             The public URL assigned to ngrok tunnel or
             None if not successful
        """
        connected = self.connect_server(FLASK_PORT)
        assert isinstance(connected, bool)
        self._connected_already = connected
        print(f'ngrok connected: {connected}')
        if connected:
            return self._public_url
        else:
            return None

    def set_account_info(self) -> bool:
        """
        Set the ngrok auth token loaded from disk

        Returns:
            True if successful, False if not
        """
        try:
            ngrok_info = pickle.load(open(NGROK_INFO_PATH, 'rb'))
            self._auth_token = ngrok_info['ngrok_auth_token']
            return True
        except FileNotFoundError:
            traceback.print_exc()
            print('There is not ngrok account info.')
            return False

    def connect_server(self, port: typing.Union[str, int]) -> bool:
        """
        Call for ngrok client to establish tunnel to ngrok server.
        This will assign unique public URL to tunnel.
        Purpose is for users to have web interface to enter phone number.

        Args:
            port: The port for ngrok to use

        Returns:
            True if successful, False if not
        """
        try:
            ngrok_config = conf.get_default()
            ngrok_config.auth_token = self._auth_token
            ngrok_tunnel = ngrok.connect(port)
            public_url = ngrok_tunnel.public_url
            assert isinstance(public_url, str)
            self._public_url = ngrok_tunnel.public_url
            return True
        except OSError:
            traceback.print_exc()
            return False
        except AssertionError:
            traceback.print_exc()
            return False
        except urllib.error.HTTPError:
            traceback.print_exc()
            return False
        except PyngrokNgrokError:
            traceback.print_exc()
            return False

    def disconnect_server(self) -> None:
        """
        Call for ngrok client to disconnect from ngrok server
        when app closes

        Returns:

        """
        if self._connected_already:
            ngrok.disconnect(self._public_url)
            tunnels = ngrok.get_tunnels()
            assert len(tunnels) == 0
            ngrok.kill()
            # self.ensure_disconnect()
            self._connected_already = False
        else:
            pass

    # def ensure_disconnect(self) -> None:
    #     """
    #     Ensure there is no ngrok process still running
    #
    #     Returns:
    #
    #     """
    #     result: subprocess.CompletedProcess = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    #     lines: typing.List[str] = result.stdout.splitlines()
    #     pid = self.get_pid(lines)
    #     if pid:
    #         subprocess.run(['kill', '-9', pid])
    #     else:
    #         return None

    # @staticmethod
    # def get_pid(lines: typing.List[str]) -> str:
    #     """
    #     Parse lines line for the PID
    #
    #     Returns:
    #          The PID as str
    #     """
    #     for line in lines:
    #         if 'ngrok' in line and 'grep' not in line:
    #             parts = line.split()
    #             pid = parts[1]
    #             print(f'Killing lingering ngrok pid: {pid}.')
    #             return pid
    #         else:
    #             continue

    @property
    def public_url(self) -> typing.Optional[str]:
        """

        Returns:
             The public ngrok URL
        """
        return self._public_url

    @property
    def connected_already(self) -> bool:
        """

        Returns:
             True if Ngrok connected, False if not
        """
        return self._connected_already


if __name__ == "__main__":
    pass
