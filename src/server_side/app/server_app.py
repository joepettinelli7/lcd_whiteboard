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
