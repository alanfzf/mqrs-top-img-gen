import openpyxl
from .dirs import get_excel_file
from .format import remove_invalid

T_NAME = 'votaciones'

def get_workbook():
    excel = None
    try:
       excel = openpyxl.load_workbook(get_excel_file())
    except Exception as e:
        raise Exception(f"Ha ocurrido un error al tratar de abrir el libro de excel: {str(e)}")
    return excel

def get_data_from_table():
    sheet = get_workbook()._sheets[0]
    table = next((table for table in sheet.tables.values() 
        if table.name == T_NAME), None)

    if table is None:
        raise Exception("No se ha encontrado la tabla llamada votaciones!")

    # we access the data in a range
    # ex: A1:BH61 this means we go from the A1 to BH61 cell
    rows = sheet[table.ref]
    # shape of the data is more or less like this
    # so every iteration we get all the values of one row
    # [User] [Val1] [Val2]      (first iteration)
    # [Alan] [10.30] [11.70]    (second iteration)
    row_list = []

    for row in rows:
        cells = []
        for cell in row:
            cells.append(cell.value)
        row_list.append(cells)

    return row_list

def get_scores_from_table(table):
    titles = table[0][2:]
    chunk_size = 30
    scores = {}

    for col, title in enumerate(titles, start=2):
        uscores = [{"user": item[1].replace('@', ''), "score": item[col]} for item in table[1:]]
        chunks = [uscores[i:i+chunk_size] for i in range(0, len(uscores), chunk_size)]
        scores[remove_invalid(title)] = chunks

    return scores

def get_values_from_col(table, col):
    # we ignore the first column as it contains the name of the data
    values = [item[col] for item in table][1:]
    return values
