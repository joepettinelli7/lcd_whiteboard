import os
import pickle
import pytest
from unittest.mock import patch

from src.server_side.backend.configs.drawing_surface_config import DrawingSurfaceConfig
from src.server_side.backend.configs.drawing_surface_config import DIR_KEY, FILE_KEY, DARK_KEY


@pytest.fixture
def ds_config_fix() -> DrawingSurfaceConfig:
    ds_config = DrawingSurfaceConfig()
    return ds_config


class TestDrawingSurfaceConfig:

    def test_setitem_(self, ds_config_fix: DrawingSurfaceConfig) -> None:
        """

        """
        set_key = "set_key"
        set_val = "set_val"
        ds_config_fix[set_key] = set_val
        assert ds_config_fix[set_key] == set_val

    def test_getitem_(self, ds_config_fix: DrawingSurfaceConfig) -> None:
        """

        """
        # Get key not there. Should catch error
        bad_key = "bad_key"
        bad_val = ds_config_fix[bad_key]
        # Add key then get
        ds_config_fix["good_key"] = "good_value"
        good_value = ds_config_fix["good_key"]
        assert good_value == "good_value"

    @pytest.mark.parametrize(["exists", "default"], [(True, False), (False, True), (False, True), (True, True)])
    def test_load_dark_mode(self, ds_config_fix: DrawingSurfaceConfig, exists: bool, default: bool) -> None:
        """

        """
        with patch('os.path.exists', return_value=exists) as patch_exist:
            mock_data = {'save_dir': 'test_dir', 'file_name': 'test.pkl', 'dark_mode': default}
            dir_val = os.path.dirname(os.path.abspath(__file__)) + '/'
            file_val = 'tmpl8ouwchk.pkl'
            pickle.dump(mock_data, open((dir_val + file_val), 'wb'))
            # Read from temp file in actual function
            ds_config_fix[FILE_KEY] = file_val
            ds_config_fix[DIR_KEY] = dir_val
            # Call function
            dark_mode = ds_config_fix.load_dark_mode(default=default)
            if patch_exist:
                assert dark_mode == mock_data['dark_mode']
            else:
                assert dark_mode == default
        os.remove((dir_val + file_val))

    @pytest.mark.parametrize(["exists", "dark"], [(True, False), (False, True)])
    def test_save(self, ds_config_fix: DrawingSurfaceConfig, exists: bool, dark: bool) -> None:
        """

        """
        dir_val = os.path.dirname(os.path.abspath(__file__)) + "/"
        file_val = 'tmpl8ouwchk.pkl'
        ds_config_fix[FILE_KEY] = file_val
        ds_config_fix[DIR_KEY] = dir_val
        ds_config_fix[DARK_KEY] = dark
        mock_data = {'save_dir': dir_val, 'file_name': file_val, 'dark_mode': dark}
        ds_config_fix.save()
        with open(dir_val + file_val, 'rb') as save_file:
            saved_data = pickle.load(save_file)
            assert mock_data == saved_data
        os.remove((dir_val + file_val))


if __name__ == "__main__":
    pass
