import pickle
import pathlib
from os import path

# folders
BASE_FOLDER = path.join(path.dirname(
    path.dirname(path.abspath(__file__))
    ), 'files')

# files
EXCEL_FILE = 'data.xlsx'
FONT_FILE = 'font.ttf'
COOKIES_FILE = 'cookies.pkl'

def get_excel_file():
    return path.join(BASE_FOLDER, EXCEL_FILE)

def get_font_file():
    return path.join(BASE_FOLDER, FONT_FILE)

def get_output_file(title, count):
    folder = path.join(BASE_FOLDER, 'output')
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    file = path.join(folder, f'{title}_{count}.png')
    return file

def cookies_exist():
    file = path.join(BASE_FOLDER, COOKIES_FILE)
    return path.exists(file)

def save_cookies(cookies):
    file = path.join(BASE_FOLDER, COOKIES_FILE)
    pickle.dump(cookies, open(file, "wb"))

def load_cookies():
    file = path.join(BASE_FOLDER, COOKIES_FILE)
    cookies = pickle.load(open(file, "rb"))
    return cookies
