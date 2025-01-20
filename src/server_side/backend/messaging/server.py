"""
    LCD Whiteboard to create touchscreen whiteboard interface and send MMS.
    Copyright (C) 2025 Joseph Pettinelli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see https://www.gnu.org/licenses/.
"""

import pickle
import threading
import time
import traceback
import typing
import socket
from PyQt5.QtCore import QThread, pyqtSignal

from src.server_side.backend.messaging.ngrok import NgrokClient
from src.server_side.backend.messaging.twilio import TwilioClient

SOCKET_PORT = 7000
SOCKET_HOST = ''


class Server(QThread):
    """
    Thread to run the server socket.
    Stopped from main thread.

    """

    should_stop_signal: pyqtSignal = pyqtSignal()
    add_recipient_signal: pyqtSignal = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()
        self._ngrok_client: NgrokClient = NgrokClient()
        self._twilio_client: TwilioClient = TwilioClient()
        self._server_condition: threading.Condition = threading.Condition()
        self._sock_address: typing.Tuple[str, int] = (SOCKET_HOST, SOCKET_PORT)
        self._sock: typing.Optional[socket.socket] = None
        self._client_conn: typing.Optional[socket.socket] = None
        self._ngrok_url: typing.Optional[str] = None
        self._should_run: bool = True
        self._recipient_added: int = -1

    def run(self) -> None:
        """
        Start the server thread.
        Handle client requests while should_run

        Returns:

        """
        while self._should_run:
            try:
                if self._sock is None:
                    self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._sock.bind(self._sock_address)
                else:
                    self.handle_client_requests()
            except socket.timeout:
                # timeout error subclasses OSError
                continue
            except OSError:
                traceback.print_exc()

    def handle_client_requests(self) -> None:
        """
        1. Set timeout for socket
        2. Listen for clients
        3. Receive message from client
        4. Send response

        Returns:

        """
        self._sock.settimeout(1)
        self._sock.listen(1)
        self.notify_flask_to_start()
        self._client_conn, client_address = self._sock.accept()
        print('Server socket accepted client connection.')
        client_data = self._client_conn.recv(1024)
        if client_data is not None:
            server_response = self.process_data(client_data)
            self._client_conn.sendall(server_response)
            self._client_conn.close()
        else:
            return None

    def process_data(self, client_data: bytes) -> bytes:
        """
        Process the client data and return response.
        Data will be ngrok url or recipient info.

        Args:
            client_data: The data received from client

        Returns:
             The response to send back to client
        """
        server_response = ''
        dict_data = pickle.loads(client_data)
        print(f"Server received: {dict_data}.")
        if 'start_ngrok' in dict_data:
            ngrok_status = self.process_ngrok_data(dict_data)
            server_response += ngrok_status
        if 'name' in dict_data and 'number' in dict_data:
            recipient_status = self.process_recipient_data(dict_data)
            server_response += recipient_status
        response_bytes = pickle.dumps(server_response)
        return response_bytes

    def process_ngrok_data(self, ngrok_data: typing.Dict[str, bool]) -> str:
        """
        Process the request from client to start ngrok

        Args:
            ngrok_data: {'start_ngrok': True}

        Returns:
             Whether ngrok started successfully or not
        """
        if ngrok_data['start_ngrok']:
            started = self.start_ngrok()
            response = f'Ngrok started: {started}.'
        else:
            response = f"Server received invalid ngrok request: {ngrok_data['start_ngrok']}."
        return response

    def start_ngrok(self) -> bool:
        """
        Start the ngrok client to connect ngrok server and create tunnel
        to Flask address

        Returns:
             True if ngrok starts successfully, False if not
        """
        if self.ngrok_client.set_account_info():
            url = self.ngrok_client.start_ngrok()
            if url is not None:
                self.twilio_client.ngrok_url = url
                return True
            else:
                return False
        else:
            return False

    def process_recipient_data(self, recipient_data: typing.Dict[str, str]) -> str:
        """
        Process request from client to add recipient.
        Wait for status of the add to get set in self._recipient
        added variable before getting response for client

        Args:
            recipient_data: {'name': name, 'number': number}

        Returns:
             Whether recipient was added successfully or not
        """
        name = recipient_data['name']
        number = recipient_data['number']
        emit_data = (name, number)
        self.add_recipient_signal.emit(emit_data)
        self.wait_for_add()
        response = self.make_recipient_response()
        # Reset back to -1 for next time
        self._recipient_added = -1
        return response

    def wait_for_add(self, max_time: float = 3.0) -> None:
        """
        Continue running until recipient add status has
        been set in this class

        Args:
            max_time: Max time to wait

        Returns:

        """
        start_wait = time.time()
        while self._recipient_added == -1:
            wait_time = time.time() - start_wait
            if wait_time >= max_time:
                return

    def make_recipient_response(self) -> str:
        """
        Get the str to send back to client / user
        based on status of adding that user to recipients

        Returns:
             Statement stating if recipient was added or not
        """
        if self._recipient_added == 0:
            response = 'Added successfully!'
        elif self._recipient_added == 1:
            response = 'Not added successfully because that name has already been added. ' \
                       'Please try a different name.'
        elif self._recipient_added == 2:
            response = 'Not added successfully because that number has already been added. ' \
                       'Please try a different number.'
        else:
            assert self._recipient_added == -1
            response = 'Error on server side adding your info. Please try again.'
        return response

    def notify_flask_to_start(self) -> None:
        """
        Notify main window that Flask can start

        Returns:

        """
        with self._server_condition:
            self._server_condition.notifyAll()

    def close_socket(self) -> None:
        """
        Close the socket

        Returns:

        """
        if self._sock:
            self._sock.close()
            self._sock = None
        else:
            pass

    @property
    def ngrok_client(self) -> NgrokClient:
        """

        Returns:
             The ngrok client
        """
        return self._ngrok_client

    @property
    def twilio_client(self) -> TwilioClient:
        """

        Returns:
             The twilio client that sends messages
        """
        return self._twilio_client

    @property
    def server_condition(self) -> threading.Condition:
        """
        Server condition used to notify Flask
        when to start

        Returns:
             The condition
        """
        return self._server_condition

    @property
    def sock(self) -> typing.Optional[socket.socket]:
        """

        Returns:
             The socket if there is one
        """
        return self._sock

    @property
    def should_run(self) -> bool:
        """
        Whether thread should be running

        Returns:
             True if thread should be running
        """
        return self._should_run

    @should_run.setter
    def should_run(self, new_status: bool) -> None:
        """
        Set whether thread should be running

        Args:
            new_status: True if thread should run

        Returns:

        """
        assert isinstance(new_status, bool)
        self._should_run = new_status

    @property
    def recipient_added(self) -> int:
        """

        Returns:
             Whether last recipient was added successfully or not.
        """
        return self._recipient_added

    @recipient_added.setter
    def recipient_added(self, new_status: int) -> None:
        """
        Called from main_window.
        The int can be:
            - -1: Not set yet
            - 0: Success
            - 1: The name has already been added
            - 2: The number has already been added

        Args:
            new_status: Whether recipient was successfully added

        Returns:

        """
        assert -1 <= new_status <= 2
        self._recipient_added = new_status


if __name__ == "__main__":
    pass
