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

current_dir = os.getcwd()
while current_dir.split('/')[-1] != 'lcd_whiteboard_github':
    current_dir = os.path.abspath(os.path.join(current_dir, '..'))
os.chdir(current_dir)
ROOT_DIR = current_dir

print("LCD Whiteboard Copyright (C) 2025 Joseph Pettinelli\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is "
      "free software, and you are welcome to redistribute it under certain conditions.\n")
