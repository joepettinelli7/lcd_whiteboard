from unittest.mock import patch
import pytest
import typing
from PyQt5.QtCore import Qt, QModelIndex

from src.server_side.backend.models.recipient_select_model import RecipientSelectModel


@pytest.fixture
def model_fix() -> RecipientSelectModel:
    model = RecipientSelectModel()
    # Already has 'Select all' recipient
    model._recipients['new_name'] = '1111111111'
    model._names.append('new_name')
    return model


class TestRecipientSelectModel:

    def test_row_count(self, model_fix: RecipientSelectModel) -> None:
        """

        """
        row_count = model_fix.rowCount()
        assert row_count == len(model_fix._recipients)

    @pytest.mark.parametrize('test_role', [Qt.DisplayRole, Qt.CheckStateRole])
    def test_data1(self, model_fix: RecipientSelectModel, test_role: int) -> None:
        """
        Test DisplayRole and UserRole
        """
        index = model_fix.index(1, 0, QModelIndex())
        data_result = model_fix.data(index, test_role)
        if test_role == Qt.DisplayRole:
            assert data_result == 'new_name'
        if test_role == Qt.UserRole:
            assert data_result == '1111111111'
        if test_role == Qt.CheckStateRole:
            assert data_result == Qt.Unchecked

    @pytest.mark.parametrize('test_checked_recipients', [{}, {'new_name': '1111111111'}])
    def test_data2(self, model_fix: RecipientSelectModel, test_checked_recipients: typing.Dict[str, str]) -> None:
        """
        Test CheckStateRole
        """
        model_fix._checked_recipients = test_checked_recipients
        index = model_fix.index(1, 0, QModelIndex())
        data_result = model_fix.data(index, Qt.CheckStateRole)
        if len(test_checked_recipients) == 0:
            assert data_result == Qt.Unchecked
        else:
            assert data_result == Qt.Checked

    @pytest.mark.parametrize('test_index', [0, 1, 1000])
    def test_data3(self, model_fix: RecipientSelectModel, test_index: int) -> None:
        """
        Test different indices
        """
        index = model_fix.index(test_index, 0, QModelIndex())
        data_result = model_fix.data(index, Qt.DisplayRole)
        if test_index == 0:
            assert data_result == 'Select all'
        elif test_index == 1:
            assert data_result == 'new_name'
        else:
            assert data_result is None

    @pytest.mark.parametrize('idx', [0, 1])
    def test_set_data1(self, model_fix: RecipientSelectModel, idx: int) -> None:
        """
        Test set checked
        """
        index = model_fix.index(idx, 0, QModelIndex())
        result = model_fix.setData(index, Qt.Checked, Qt.CheckStateRole)
        if idx == 0:
            assert model_fix._checked_recipients == {'Select all': '', 'new_name': '1111111111'}
        else:
            assert model_fix._checked_recipients == {'new_name': '1111111111'}
        assert result

    @pytest.mark.parametrize('idx', [1, 0])
    def test_set_data2(self, model_fix: RecipientSelectModel, idx: int) -> None:
        """
        Test set unchecked
        """
        model_fix._checked_recipients = {'Select all': '', 'new_name': '1111111111'}
        index = model_fix.index(idx, 0, QModelIndex())
        result = model_fix.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        if idx == 0:
            assert len(model_fix._checked_recipients) == 0
        else:
            assert model_fix._checked_recipients == {'Select all': ''}
        assert result

    @pytest.mark.parametrize('name', ['Select all', 'new_name'])
    def test_handle_checked(self, model_fix: RecipientSelectModel, name: str) -> None:
        """

        """
        with patch.object(model_fix, 'add_all_to_checked') as patch_add_all:
            model_fix.handle_checked(name)
            if name == 'Select all':
                patch_add_all.assert_called_once()
            else:
                patch_add_all.assert_not_called()
                assert model_fix._checked_recipients == {'new_name': '1111111111'}

    @pytest.mark.parametrize('name', ['Select all', 'new_name'])
    def test_handle_unchecked(self, model_fix: RecipientSelectModel, name: str) -> None:
        """

        """
        model_fix._checked_recipients = {'Select all': '', 'new_name': '1111111111'}
        model_fix.handle_unchecked(name)
        if name == 'Select all':
            assert len(model_fix._checked_recipients) == 0
        else:
            assert model_fix._checked_recipients == {'Select all': ''}

    def test_add_all_to_checked(self, model_fix: RecipientSelectModel) -> None:
        """

        """
        num_recipients = len(model_fix._recipients)
        model_fix.add_all_to_checked()
        assert len(model_fix._checked_recipients) == num_recipients

    def test_flags(self, model_fix: RecipientSelectModel) -> None:
        """

        """
        flag = model_fix.flags(QModelIndex())
        assert flag == Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

    @pytest.mark.parametrize('valid_status', [0, 1, 2])
    def test_add_recipient(self, model_fix: RecipientSelectModel, valid_status: int) -> None:
        """
        Test name valid and not valid
        """
        with patch.object(model_fix, 'is_recipient_valid') as patch_valid_status:
            patch_valid_status.return_value = valid_status
            with patch.object(model_fix, 'beginInsertRows') as patch_begin:
                with patch.object(model_fix, 'endInsertRows') as patch_end:
                    row_count = model_fix.rowCount()
                    add_result = model_fix.add_recipient('test_name', '1')
                    if valid_status == 0:
                        # Will add 1 to front of number for US
                        assert model_fix._recipients['test_name'] == '11'
                        assert list(model_fix._recipients.keys()) == model_fix._names
                        patch_begin.assert_called_once_with(QModelIndex(), row_count, row_count)
                        patch_end.assert_called_once()
                    else:
                        patch_begin.assert_not_called()
                        patch_end.assert_not_called()
                    assert add_result == valid_status

    @pytest.mark.parametrize(['name_valid', 'num_valid'], [(True, True), (True, False), (False, True)])
    def test_is_recipient_valid(self, model_fix: RecipientSelectModel, name_valid: bool, num_valid: bool) -> None:
        """

        """
        with patch.object(model_fix, 'is_name_valid') as patch_name_valid:
            with patch.object(model_fix, 'is_number_valid') as patch_number_valid:
                patch_name_valid.return_value = name_valid
                patch_number_valid.return_value = num_valid
                valid_status = model_fix.is_recipient_valid('test_name', '1')
                if name_valid and num_valid:
                    assert valid_status == 0
                elif name_valid and not num_valid:
                    assert valid_status == 2
                else:
                    assert valid_status == 1

    @pytest.mark.parametrize('new_name', ['new_name', 'NEW_NAME', 'another_name'])
    def test_is_name_valid(self, model_fix: RecipientSelectModel, new_name: str) -> None:
        """

        """
        valid = model_fix.is_name_valid(new_name)
        if new_name == 'another_name' or new_name == 'NEW_NAME':
            assert valid
        else:
            assert not valid

    @pytest.mark.parametrize('new_number', ['911', '11111111111', '1111111111', 'new_name', '2222222222'])
    def test_is_number_valid(self, model_fix: RecipientSelectModel, new_number: str) -> None:
        """

        """
        valid = model_fix.is_number_valid(new_number)
        if new_number == '2222222222':
            assert valid
        else:
            assert not valid

    def test_checked_recipients_getter(self, model_fix: RecipientSelectModel) -> None:
        """

        """
        assert model_fix._checked_recipients is model_fix.checked_recipients
        assert isinstance(model_fix.checked_recipients, dict)


if __name__ == "__main__":
    pass
