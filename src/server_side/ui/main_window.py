import traceback
import typing
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from src.server_side.backend.messaging.client_controller import ClientController
from src.server_side.ui.drawing_surface import DrawingSurface
from src.server_side.ui.toolbar_widgets.drawing_toolbar import DrawingToolBar
from src.server_side.backend.messaging.server import Server
from src.server_side.ui.toolbar_widgets.qr_widget import QrWidget
from src.server_side.ui.toolbar_widgets.send_dialog import SendDialog

IMAGE_PAGE = "wb_image"


class WhiteboardMW(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._client_controller: ClientController = ClientController()
        self._drawing_surface: DrawingSurface = DrawingSurface()
        self._drawing_toolbar: DrawingToolBar = DrawingToolBar()
        self._qr_widget: QrWidget = QrWidget()
        self._send_dialog: SendDialog = SendDialog(self)
        self._server: typing.Optional[Server] = None
        self.setCentralWidget(self._drawing_surface)
        self.addToolBar(self._drawing_toolbar)

    def connect_signals(self) -> None:
        """
        Connect toolbar action signals and slots. This function is only called
        once so that signals do not get connected multiple times.

        Returns:

        """
        # Color combobox selection -> update drawing surface color
        self._drawing_toolbar.color_combobox.currentIndexChanged.connect(self.update_color_slot)
        # Send whiteboard button -> show send dialog
        self._drawing_toolbar.send_action.triggered.connect(self.show_send_dialog_slot)
        # Send dialog closed -> send whiteboard to recipients
        self._send_dialog.finished.connect(self.send_dialog_finished_slot)
        # Undo line button clicked -> drawing surface remove line
        self._drawing_toolbar.undo_line_action.triggered.connect(self._drawing_surface.undo_line_slot)
        # QR button clicked -> show qr widget
        self._drawing_toolbar.show_qr_action.triggered.connect(self.show_qr_slot)
        # Dark mode toggle button -> drawing surface change color
        self._drawing_toolbar.dark_mode_action.triggered.connect(self._drawing_surface.toggle_dark_slot)

    def set_server(self) -> bool:
        """
        Set the server. Called from server application

        Returns:
            True if twilio account info found, False if twilio account
            info is not found
        """
        self._server = Server()
        self._server.should_stop_signal.connect(self.stop_all)
        self._server.add_recipient_signal.connect(self.add_recipient_slot)
        return self._server.twilio_client.set_account_info()

    def show_mw(self) -> None:
        """
        Show the main window.
        Set the size of drawing surface to be size of main window.

        Returns:

        """
        mw_geom = self.geometry()
        self._drawing_surface.setGeometry(mw_geom)
        self.show()
        self.raise_()

    def start_all(self, server_set_success: bool) -> None:
        """
        Start the server thread and client app.
        Called when app starts.

        Args:
            server_set_success: Whether server was successfully set

        Returns:

        """
        if server_set_success:
            with self._server.server_condition:
                self.start_server()
                # Wait for server to start listening
                # before starting ngrok
                self._server.server_condition.wait(1)
                self._client_controller.start_client()
        else:
            print('Not starting server.')

    def start_server(self) -> None:
        """
        Start the server thread

        Returns:

        """
        assert self._server is not None
        self._server.should_run = True
        self._server.start()

    def update_color_slot(self) -> None:
        """
        Slot connected when user changes new color

        Returns:

        """
        color = self._drawing_toolbar.color_combobox.get_color()
        self._drawing_surface.selected_color = color

    def show_send_dialog_slot(self) -> None:
        """
        Slot connected when 'Send' action is triggered

        Returns:

        """
        self._send_dialog.open()

    def send_dialog_finished_slot(self, result: int) -> None:
        """
        Slot called when send dialog is finished

        Args:
            result: The result from dialog

        Returns:

        """
        if result == QDialog.DialogCode.Accepted:
            numbers = self._send_dialog.recipient_view.get_checked_numbers()
            self.send_whiteboard(numbers)
        else:
            pass

    def send_whiteboard(self, numbers: typing.List[str]) -> None:
        """
        Called after send dialog is accepted

        Args:
            numbers: The numbers to send whiteboard to

        Returns:

        """
        save_success = self._drawing_surface.save_whiteboard_image()
        if save_success:
            self._server.twilio_client.send_to_all(IMAGE_PAGE, numbers)
        else:
            print('Image was not saved.')

    def add_recipient_slot(self, recipient_info: typing.Tuple[str, str]) -> None:
        """
        Slot connected from when potential recipient submits their info.
        Set the status_val in server to send back to client.

        Args:
            recipient_info: The name and phone number

        Returns:

        """
        name = recipient_info[0]
        number = recipient_info[1]
        status_val = self._send_dialog.recipient_view.add_recipient(name, number)
        self._server.recipient_added = status_val

    def show_qr_slot(self) -> None:
        """
        Slot connected when 'Show QR' action is clicked

        Returns:

        """
        try:
            public_url = self._server.ngrok_client.public_url
            assert self._server.ngrok_client.connected_already
            assert public_url is not None
            self._qr_widget.set_qr_code(public_url)
            self._qr_widget.show()
        except AssertionError:
            traceback.print_exc()
            self.show_message('QR not available because ngrok did not start. Potentially because no ngrok account '
                              'info was found.')

    def show_message(self, message: str) -> None:
        """
        Show message to user

        Args:
            message: The message to show

        Returns:

        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Information")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        _ = msg_box.exec_()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Called when the window is about to close.

        Args:
            event: The close event

        Returns:

        """
        self.stop_all()

    def stop_all(self) -> None:
        """
        Stop the server thread and close socket.
        Order is important.

        1. Stop ngrok
        2. Stop the client app
        3. Stop server socket thread and wait
        4. Close the server socket
        5. Delete the wb_image
        6. Save the drawing surface config

        Returns:

        """
        self._server.ngrok_client.disconnect_server()
        self._client_controller.stop_client()
        self._server.should_run = False
        self._server.wait()
        self._server.close_socket()
        self._drawing_surface.delete_wb_image()
        self._drawing_surface.save_config()


if __name__ == "__main__":
    pass
