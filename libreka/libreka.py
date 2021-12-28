import re
from pathlib import Path

import pandas as pd

from engineer import sql_writer


def get_table_names(sheet_name_originals):
    tables = ('e_book', 'a_book', 'free', 'sub')
    good_for_table_names = dict(zip(sheet_name_originals, tables))
    return good_for_table_names


def get_comparable_names(columns_list):
    prog = re.compile(r"\.[0-9]$")
    for index, col in enumerate(columns_list):
        z = re.search(prog, col)
        if z:
            columns_list[index] = col[:-2]
    return columns_list


def check_sheet_df(sheet, df):
    filename = 'sheet_fields_libreka.txt'
    file_path = Path.cwd() / 'libreka' / filename
    error = 0
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:  # read list of expected column names
            lines = f.readlines()
            sheets = [line.strip().split(';')[0] for line in lines]
            fields = [line.strip().split(';')[1] for line in lines]
            for index, s in enumerate(sheets):
                if s == sheet:
                    df_field_names = get_comparable_names(list(df.columns))
                    if not (fields[index].split(',') == df_field_names):  # compare two lists
                        error = 1
                        break
    except FileNotFoundError as fnfe:
        print(f"but CAN'T find field-names file: {filename} to check fields in sheet:\n error {fnfe}")
        error = 2
    return error


def check_file_sheet_names(f, sheet_name_originals):
    try:
        sheets_in_file = get_sheets(f)
        for sheet in sheets_in_file:
            if sheet not in sheet_name_originals:
                print(f'Alert, unknown sheet "{sheet}" in {f}: ')
                return 1
        return 0
    except ValueError as ve:
        print(f'File is open, unreadable, error: {ve}')
        return 2


def get_sheets(f):
    sheets_in_file = {}
    try:
        sheets_in_file = pd.read_excel(f, sheet_name=None, header=0)
    except TypeError as e:
        print(f'Excel read had produced an error: {e}')
    return sheets_in_file


def main(dirpath):
    p = Path(dirpath)
    expected_sheet_names = ('E-Book-Verkäufe', 'Hörbuch-Verkäufe', 'Kostenlostitel', 'Abo und Flatrate')
    excel_files = [item for item in p.iterdir() if item.is_file() and item.suffix == '.xlsx']  # list
    good_for_table_names = get_table_names(expected_sheet_names)  # dict

    for f in excel_files:
        sheets_in_file = get_sheets(f)  # dict
        sheet_error = check_file_sheet_names(f, expected_sheet_names)
        if sheet_error == 0:
            print(f'Sheets are as expected in file {f}')
        elif sheet_error == 1:
            print(f"There's some weird shit going on in {f}, unknown sheet in file.\n{sheets_in_file.keys()}")
            print('Signing off... Clean the DB now!!!')
            return
        elif sheet_error == 2:
            print('File read error, signing off...')
            return
        # check fields in each sheet dict
        for sheet, df in sheets_in_file.items():
            field_error = check_sheet_df(sheet, df)  # check fields in sheet
            if field_error == 1:
                print(f"ERROR!!! \nColumns in file `{f.name}`, sheet `{sheet}` NOT matching the expected.")
                print('not going to write any further to db. Clean up db!\nSigning off...')
                return
            elif field_error == 2:
                print('Checking field names failed, no Libreka field reference file found, signing off...')
                return
            else:
                table_name = 'libreka_' + good_for_table_names[sheet]
                sql_writer.write_to_db(df, table_name, 'append', '19')  # select DB here


if __name__ == '__main__':
    main('/Users/frank/pd/sales_report/16_libreka')
