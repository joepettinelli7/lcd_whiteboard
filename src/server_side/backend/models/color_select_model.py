import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QPersistentModelIndex, Qt, QAbstractListModel
from PyQt5.QtGui import QColor, QPixmap, QIcon


class ColorSelectModel(QAbstractListModel):

    def __init__(self) -> None:
        super().__init__()
        self._colors: typing.List[str] = ['black', 'red', 'orange', 'yellow',
                                          'green', 'blue', 'purple', 'white']

    def rowCount(self, parent: typing.Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        """

        Args:
            parent: Usually no parent for a list model

        Returns:
            The number of rows in model (same as number colors)
        """
        return len(self._colors)

    def data(self, index: typing.Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> typing.Any:
        """
        Data in model

        Args:
            index: The index of the color in colors list
            role: The role of the data

        Returns:

        """
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            color = self._colors[index.row()]
            return color
        if role == Qt.UserRole:
            color = self._colors[index.row()]
            return QColor(color)
        if role == Qt.DecorationRole:
            color = self._colors[index.row()]
            pixmap = QPixmap(15, 15)
            pixmap.fill(QColor(color))
            return QIcon(pixmap)
        return None

    def flags(self, index: typing.Union[QModelIndex, QPersistentModelIndex]) -> QtCore.Qt.ItemFlags:
        """

        Args:
            index: The index of the color in colors list

        Returns:
            The item should be selectable and enabled
        """
        return QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled


if __name__ == "__main__":
    pass
