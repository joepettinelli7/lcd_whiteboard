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

import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QPersistentModelIndex, QAbstractListModel, Qt


class RecipientSelectModel(QAbstractListModel):

    def __init__(self) -> None:
        super().__init__()
        self._recipients: typing.Dict[str, str] = {'Select all': ''}
        self._checked_recipients: typing.Dict[str, str] = {}
        self._names: typing.List[str] = list(self._recipients.keys())

    def rowCount(self, parent: typing.Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        """

        Args:
            parent: Usually no parent for a list model

        Returns:
            The number of rows in model (same as number of recipients)
        """
        return len(self._recipients)

    def data(self, index: typing.Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> typing.Any:
        """
        Data in model

        Args:
            index: The index of the recipient in recipients list
            role: The role of the data

        Returns:

        """
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            name = self._names[index.row()]
            return name
        if role == Qt.UserRole:
            name = self._names[index.row()]
            number = self._recipients[name]
            return number
        if role == Qt.CheckStateRole:
            name = self._names[index.row()]
            if name in self._checked_recipients:
                return Qt.Checked
            else:
                return Qt.Unchecked
        return None

    def setData(self, index: typing.Union[QModelIndex, QPersistentModelIndex], value: typing.Any,
                role: int = ...) -> bool:
        """
        Needed to set items checked by user

        Args:
            index: The index of the data
            value: The value (checked or unchecked)
            role: The role of the data (checkStateRole)

        Returns:
             True if data changed successfully
        """
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole:
            name = self._names[index.row()]
            if value == Qt.Checked:
                self.handle_checked(name)
            if value == Qt.Unchecked:
                self.handle_unchecked(name)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return True

    def handle_checked(self, name: str) -> None:
        """
        Update model when item is checked

        Args:
            name: The name that was checked

        Returns:

        """
        if name == 'Select all':
            self.add_all_to_checked()
        else:
            self._checked_recipients[name] = self._recipients[name]

    def handle_unchecked(self, name: str) -> None:
        """
        Update model when item is unchecked

        Args:
            name: The name that was unchecked

        Returns:

        """
        if name == 'Select all':
            self._checked_recipients.clear()
        else:
            if name in self._checked_recipients:
                del self._checked_recipients[name]

    def add_all_to_checked(self) -> None:
        """
        Called when 'Select all' is checked.
        Add all recipients to checked.

        Returns:

        """
        self._checked_recipients.clear()
        for name, number in self._recipients.items():
            self._checked_recipients[name] = number

    def flags(self, index: typing.Union[QModelIndex, QPersistentModelIndex]) -> QtCore.Qt.ItemFlag:
        """

        Args:
            index: The index of the recipient in recipients list

        Returns:
            The item should be selectable, editable, and enabled
        """
        return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

    def add_recipient(self, new_name: str, new_number: str) -> int:
        """
        Add the name and number of recipient to recipients dict and names list

        Args:
            new_name: The name of recipient
            new_number: The number of recipient

        Returns:
            - 0: Success
            - 1: The name has already been added
            - 2: The number has already been added
        """
        recipient_valid = self.is_recipient_valid(new_name, new_number)
        if recipient_valid == 0:
            row_count = self.rowCount()
            self.beginInsertRows(QModelIndex(), row_count, row_count)
            new_number = f'1{new_number}'
            self._recipients[new_name] = new_number
            self._names = list(self._recipients.keys())
            self.endInsertRows()
            return 0
        else:
            return recipient_valid

    def is_recipient_valid(self, new_name: str, new_number: str) -> int:
        """
        Check if the number should be added to self._recipients.
        Don't allow duplicate names or numbers.

        Args:
            new_name: The recipient name
            new_number: The recipient number

        Returns:
            - 0: Success
            - 1: The name has already been added
            - 2: The number has already been added
        """
        if self.is_name_valid(new_name):
            if self.is_number_valid(new_number):
                return 0
            else:
                return 2
        else:
            return 1

    def is_name_valid(self, new_name: str) -> bool:
        """
        Check if the name should be added to self._recipients.

        Args:
            new_name: The recipient name

        Returns:
            True if valid name, False if not
        """
        if new_name in self._recipients.keys():
            return False
        else:
            return True

    def is_number_valid(self, new_number: str) -> bool:
        """
        Check if the number should be added to self._recipients.

        Args:
            new_number: The recipient number

        Returns:
            True if valid number, False if not
        """
        if new_number in self._recipients.values():
            return False
        if f'1{new_number}' in self._recipients.values():
            return False
        if not new_number.isdigit():
            return False
        if len(new_number) != 10:
            return False
        return True

    @property
    def checked_recipients(self) -> typing.Dict[str, str]:
        """

        Returns:
            The recipients that have been checked by user
        """
        return self._checked_recipients


if __name__ == "__main__":
    pass
