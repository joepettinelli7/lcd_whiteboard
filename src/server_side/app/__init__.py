import os

current_dir = os.getcwd()
while current_dir.split('/')[-1] != 'lcd_whiteboard_github':
    current_dir = os.path.abspath(os.path.join(current_dir, '..'))
os.chdir(current_dir)
ROOT_DIR = current_dir
