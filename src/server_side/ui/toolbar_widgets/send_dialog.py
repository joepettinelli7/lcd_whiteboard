import typing
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtWidgets import QListView, QVBoxLayout, QPushButton, QDialog, QHBoxLayout

from src.server_side.backend.models.recipient_select_model import RecipientSelectModel


class RecipientSelectListView(QListView):
    """
    The list view for user to select recipients

    """

    def __init__(self) -> None:
        super().__init__()
        self._cb_model: RecipientSelectModel = RecipientSelectModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self._cb_model)
        self.setModel(self.proxy_model)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)
        self.setToolTip("Select a recipient")

    def add_recipient(self, new_name: str, new_number: str) -> int:
        """
        Add a new recipient to model

        Args:
            new_name: Name of recipient
            new_number: Number of recipient

        Returns:
            - 0: Success
            - 1: The name has already been added
            - 2: The number has already been added
        """
        status_val = self.cb_model.add_recipient(new_name=new_name, new_number=new_number)
        return status_val

    def get_checked_numbers(self) -> typing.List[str]:
        """
        Get phone numbers for twilio to send image to

        Returns:
             The numbers
        """
        checked_recipients = self.cb_model.checked_recipients
        numbers = list(checked_recipients.values())
        valid_numbers = [number for number in numbers if number != '']
        return valid_numbers

    @property
    def cb_model(self) -> RecipientSelectModel:
        """

        Returns:
             The recipient select model behind this combobox
        """
        return self._cb_model


class SendDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._layout = QVBoxLayout(self)
        self._recipient_view = RecipientSelectListView()
        # Buttons
        self._send_button = QPushButton('Send')
        self._cancel_button = QPushButton('Cancel')
        self._send_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        h_button_layout = self.setup_button_layout()
        # Layout
        self._layout.addWidget(self._recipient_view)
        self._layout.addLayout(h_button_layout)
        self.setLayout(self._layout)

    def setup_button_layout(self) -> QHBoxLayout:
        """
        Make layout for buttons

        Returns:

        """
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._cancel_button)
        button_layout.addWidget(self._send_button)
        return button_layout

    @property
    def recipient_view(self) -> RecipientSelectListView:
        """

        Returns:
             The list view to select recipient
        """
        return self._recipient_view


if __name__ == "__main__":
    pass
