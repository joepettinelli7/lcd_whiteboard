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

import socket
import pickle
import typing
from flask import Flask, render_template, request, send_from_directory, Response, jsonify

SOCKET_PORT = 7000
FLASK_PORT = 6000
SOCKET_HOST = ''


class ClientApp(Flask):
    """
    Client app to the server side app for coordinating
    running Flask, but also the server to the Flask web
    page. Sort of an API for the server side app.
    """

    def __init__(self, import_name: str = "__main__") -> None:
        super().__init__(import_name=import_name)

    def start_client_app(self) -> None:
        """
        Start the client app responsible for controlling the
        Flask app for users to interface with lcd whiteboard

        Returns:

        """
        self.set_routes()
        self.server_start_ngrok()
        self.run(port=FLASK_PORT, debug=False)

    def set_routes(self) -> None:
        """
        Set up the routes for HTML page.

        Returns:

        """
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/submit', 'submit', self.submit, methods=['POST'])
        self.add_url_rule('/wb_image', 'wb_image', self.serve_image)

    def server_start_ngrok(self) -> None:
        """
        Let server know that client app is running
        and that ngrok should create tunnel now

        Returns:

        """
        message = {'start_ngrok': True}
        _ = self.send_recv(message)

    @staticmethod
    def index() -> str:
        """
        Render user facing ui

        Returns:

        """
        return render_template('client_app_template.html')

    def submit(self) -> Response:
        """
        Called when user submits information

        Returns:
             Statement stating user successfully added or not
        """
        name = request.form['name']
        number = request.form['phone_number']
        info = {'name': name, 'number': number}
        response = self.send_recv(info)
        return jsonify(response=response)

    @staticmethod
    def serve_image() -> Response:
        """
        Server the image to be sent by twilio on server side

        Returns:

        """
        return send_from_directory('static', 'wb_image.png')

    @staticmethod
    def send_recv(client_message: typing.Dict[str, typing.Any]) -> typing.Optional[str]:
        """
        Send message to server and get response

        Args:
            client_message: The message to send

        Returns:
             The response from server
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SOCKET_HOST, SOCKET_PORT))
            print('Client socket connected server socket.')
            pkl_message = pickle.dumps(client_message)
            sock.sendall(pkl_message)
            server_response = sock.recv(1024)
            str_response = pickle.loads(server_response)
            print(f"Client received: {str_response}.")
            sock.close()
            return str_response
        except ConnectionRefusedError:
            print('Connection refused because server not started.')
            return None


def client_process_target() -> None:
    """
    Target for the multiprocess module

    Returns:

    """
    client_app = ClientApp(__name__)
    client_app.start_client_app()


if __name__ == "__main__":
    app = ClientApp(__name__)
    app.start_client_app()
