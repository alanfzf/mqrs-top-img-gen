import pathlib
from os import path

# folders
BASE_DIR = path.dirname(path.abspath(__file__))
FILES_FOLDER = path.join(path.dirname(BASE_DIR), 'files')

# files
EXCEL_FILE = 'data.xlsx'
FONT_FILE = 'font.ttf'

def get_excel_file():
    return path.join(FILES_FOLDER, EXCEL_FILE)

def get_font_file():
    return path.join(FILES_FOLDER, FONT_FILE)

def get_output_file(title, count):
    folder = path.join(FILES_FOLDER, 'output')
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    file = path.join(folder, f'{title}_{count}.png')
    return file
