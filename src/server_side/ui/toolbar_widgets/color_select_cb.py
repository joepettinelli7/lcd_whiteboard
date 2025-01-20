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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox

from src.server_side.backend.models.color_select_model import ColorSelectModel


class ColorSelectCb(QComboBox):

    def __init__(self) -> None:
        super().__init__()
        self._cb_model: ColorSelectModel = ColorSelectModel()
        self.setModel(self._cb_model)
        self.setToolTip("Select a color")

    def get_color(self) -> QColor:
        """
        Get the color for the currently selected index

        Returns:
             The color currently selected by user
        """
        index = self.currentIndex()
        model_index = self.cb_model.index(index)
        color = self.cb_model.data(model_index, Qt.UserRole)
        return color

    @property
    def cb_model(self) -> ColorSelectModel:
        """

        Returns:
             The color select model b behind this combobox
        """
        return self._cb_model


if __name__ == "__main__":
    pass
