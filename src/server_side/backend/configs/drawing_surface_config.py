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

import os
import pickle
import typing

DIR_KEY: str = 'save_dir'
FILE_KEY: str = 'file_name'
DARK_KEY: str = 'dark_mode'


class DrawingSurfaceConfig(dict):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self[DIR_KEY] = os.path.dirname(os.path.abspath(__file__))
        self[FILE_KEY] = 'ds_config.pkl'
        self[DARK_KEY] = self.load_dark_mode()

    def __setitem__(self, key: str, value) -> None:
        """
        Set config items.
        Save to file after being modified

        Args:
            key: Config key
            value: Config value

        Returns:

        """
        super().__setitem__(key, value)

    def __getitem__(self, key: typing.Any) -> typing.Any:
        """
        Get value for key

        Args:
            key: The item to get

        Returns:
             The value for key
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            print(f"KeyError: {key} does not exist!")

    def load_dark_mode(self, default: bool = False) -> bool:
        """
        Load the dark mode config value from disk

        Args:
            default: Return this value if error

        Returns:
             Whether the whiteboard should be dark mode
        """
        full_path = os.path.join(self[DIR_KEY], self[FILE_KEY])
        if os.path.exists(full_path):
            with open(full_path, 'rb') as file:
                config = pickle.load(file)
                return config[DARK_KEY]
        else:
            return default

    def save(self) -> None:
        """
        Save the config to a file on disk.

        Returns:

        """
        if not os.path.exists(self[DIR_KEY]):
            os.mkdir(self[DIR_KEY])
        full_path = os.path.join(self[DIR_KEY], self[FILE_KEY])
        with open(full_path, 'wb') as save_file:
            pickle.dump(self, save_file)


if __name__ == "__main__":
    pass
