import openpyxl
from util import util

TABLE_NAME = 'Votaciones'

class UserScore:

   def __init__(self, name, score):
    self.name = name
    self.score = score



def sanitize_values(value):
    if type(value) == str:
        return value.replace('@', '')
    return value

def search_table(sheet):
    tables = sheet.tables
    for table in tables.values():
        if table.name == TABLE_NAME:
            return table
    return None

def extract_data():
    rows_list = []
    try:
        wb = openpyxl.load_workbook("./files/excel/data.xlsx")
        ws = wb._sheets[0]
        table = search_table(ws)
        data = ws[table.ref]

        for row in data:
            cols = []
            for col in row:
                cols.append(sanitize_values(col.value))
            rows_list.append(cols)
    except Exception as e:
        print(e)

    # worth noting that the first row contains 
    # the name of all the columns in the table
    return rows_list

def get_formatted_data(data):
    titles = data[0][2:]
    # the size of each chunk of data
    csize = 30
    fdata = {}

    for id, title in enumerate(titles, start=2):
        score = [item[id] for item in data[1:]]
        user = [item[1] for item in data[1:]]
        temp = [UserScore(user[i], score[i]) for i in range(len(score))]
        split = [temp[i:i+csize] for i in range(0, len(temp), csize)]
        fdata[util.remove_invalid(title)] = split
    return fdata

def get_values_from_col(values, col_num):
    # we ignore the first row because it contains
    # the name of the column
    lst = [item[col_num] for item in values]
    return lst
