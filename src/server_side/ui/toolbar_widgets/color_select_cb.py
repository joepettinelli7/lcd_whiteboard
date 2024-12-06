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
