import sys
import typing
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

from src.server_side.ui.main_window import WhiteboardMW


class ServerApp(QApplication):

    def __init__(self, sys_argv: typing.List[str]) -> None:
        super().__init__(sys_argv)

    def init_success(self) -> bool:
        """
        For testing purposes

        Returns:
            True if init successful
        """
        if self:
            return True


if __name__ == "__main__":
    server_app = ServerApp(sys.argv)
    mw = WhiteboardMW()
    geom: QRect = server_app.primaryScreen().geometry()
    mw.setGeometry(geom)
    mw.connect_signals()
    set_success = mw.set_server()
    mw.show_mw()
    if set_success:
        mw.start_all()
    else:
        mw.show_message('Some functions will be disabled because server did not start. '
                        'Potentially because no twilio account info was found.')
    sys.exit(server_app.exec())
