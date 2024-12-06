import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction

from src.server_side.app import ROOT_DIR
from src.server_side.ui.toolbar_widgets.color_select_cb import ColorSelectCb


class DrawingToolBar(QToolBar):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        # The combobox to choose a color
        self._color_combobox: ColorSelectCb = ColorSelectCb()
        self.addWidget(self._color_combobox)
        # Action to send the whiteboard image to recipients
        self._send_action = self.make_send_action()
        self.addAction(self._send_action)
        # Action to undo a line
        self._undo_line_action = self.make_undo_action()
        self.addAction(self._undo_line_action)
        # QR code to ngrok URL
        self._show_qr_action = self.make_qr_action()
        self.addAction(self._show_qr_action)
        # Action to toggle drawing surface dark mode
        self._dark_mode_action = self.make_dark_mode_action()
        self.addAction(self._dark_mode_action)

    def make_send_action(self) -> QAction:
        """
        Make the QAction for sending messages

        Returns:
             The action
        """
        icon = self.load_send_icon()
        action = QAction(icon, 'Send whiteboard', self)
        action.setIconVisibleInMenu(True)
        return action

    def make_undo_action(self) -> QAction:
        """
        Make the QAction for undo line

        Returns:
             The action
        """
        icon = self.load_undo_icon()
        action = QAction(icon, 'Undo line', self)
        action.setIconVisibleInMenu(True)
        return action

    def make_qr_action(self) -> QAction:
        """
        Make the QAction for showing QR

        Returns:
             The action
        """
        icon = self.load_qr_icon()
        action = QAction(icon, 'Show QR', self)
        action.setIconVisibleInMenu(True)
        return action

    def make_dark_mode_action(self) -> QAction:
        """
        Make the QAction for dark mode

        Returns:
             The action
        """
        icon = self.load_dark_mode_icon()
        action = QAction(icon, 'Dark mode', self)
        action.setToolTip('Toggle dark mode')
        action.setIconVisibleInMenu(True)
        return action

    @staticmethod
    def load_send_icon() -> QIcon:
        """
        Load the send icon for toolbar

        Returns:
            The icon
        """
        icon_path = os.path.join(ROOT_DIR, 'src', 'server_side', 'ui', 'toolbar_widgets', 'icons', 'send_icon.png')
        icon = QIcon(icon_path)
        return icon

    @staticmethod
    def load_undo_icon() -> QIcon:
        """
        Load the undo action for toolbar

        Returns:
            The icon
        """
        icon_path = os.path.join(ROOT_DIR, 'src', 'server_side', 'ui', 'toolbar_widgets', 'icons', 'undo_icon.png')
        icon = QIcon(icon_path)
        return icon

    @staticmethod
    def load_qr_icon() -> QIcon:
        """
        Load the QR icon for toolbar

        Returns:
            The icon
        """
        icon_path = os.path.join(ROOT_DIR, 'src', 'server_side', 'ui', 'toolbar_widgets', 'icons', 'qr_icon.png')
        icon = QIcon(icon_path)
        return icon

    @staticmethod
    def load_dark_mode_icon() -> QIcon:
        """
        Load the dark mode icon for toolbar

        Returns:
            The icon
        """
        icon_path = os.path.join(ROOT_DIR, 'src', 'server_side', 'ui', 'toolbar_widgets', 'icons', 'dark_mode_icon.png')
        icon = QIcon(icon_path)
        return icon

    @property
    def color_combobox(self) -> ColorSelectCb:
        """

        Return:
            The combobox to choose color
        """
        return self._color_combobox

    @property
    def send_action(self) -> QAction:
        """

        Return:
            The 'Send' action to send messages
        """
        return self._send_action

    @property
    def undo_line_action(self) -> QAction:
        """

        Return:
            The 'Undo' action to undo line
        """
        return self._undo_line_action

    @property
    def show_qr_action(self) -> QAction:
        """

        Return:
            The 'Show QR' action to show QR code
        """
        return self._show_qr_action

    @property
    def dark_mode_action(self) -> QAction:
        """

        Return:
            The dark mode action to toggle drawing surface dark mode
        """
        return self._dark_mode_action


if __name__ == "__main__":
    pass
