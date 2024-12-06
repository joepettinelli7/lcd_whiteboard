import pytest
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QIcon, QColor
from pytestqt.qtbot import QtBot

from src.server_side.backend.models.color_select_model import ColorSelectModel


@pytest.fixture
def model_fix() -> ColorSelectModel:
    model = ColorSelectModel()
    return model


class TestColorSelectModel:

    def test_row_count(self, model_fix: ColorSelectModel) -> None:
        """

        """
        row_count = model_fix.rowCount()
        assert row_count == len(model_fix._colors)

    @pytest.mark.parametrize('test_role', [Qt.DisplayRole, Qt.UserRole, Qt.DecorationRole])
    def test_data1(self, model_fix: ColorSelectModel, test_role: int, qtbot: QtBot) -> None:
        """
        Test different roles
        """
        index = model_fix.index(0, 0, QModelIndex())
        data_result = model_fix.data(index, test_role)
        if test_role == Qt.DisplayRole:
            assert data_result == 'black'
        if test_role == Qt.UserRole:
            assert data_result == QColor('black')
        if test_role == Qt.DecorationRole:
            assert isinstance(data_result, QIcon)

    @pytest.mark.parametrize('test_index', [0, 1000])
    def test_data2(self, model_fix: ColorSelectModel, test_index: int) -> None:
        """
        Test different indices
        """
        index = model_fix.index(test_index, test_index, QModelIndex())
        data_result = model_fix.data(index, Qt.DisplayRole)
        if test_index == 0:
            assert data_result == 'black'
        else:
            assert data_result is None

    def test_flags(self, model_fix: ColorSelectModel) -> None:
        """

        """
        flag = model_fix.flags(QModelIndex())
        assert flag == QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled


if __name__ == "__main__":
    pass
