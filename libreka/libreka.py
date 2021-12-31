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


def get_fields_diff(incoming, etalon):
    diff = lambda l1, l2: [x for x in l1 if x not in l2]
    diff2 = lambda l1, l2: [x for x in l2 if x not in l1]
    res1 = diff(incoming, etalon) + diff(etalon, incoming)
    res2 = diff2(incoming, etalon) + diff2(etalon, incoming)
    return res1 + res2


def check_sheet_df(sheet, df):
    difference = []
    filename = 'sheet_fields_libreka.txt'
    file_path = Path.cwd() / 'libreka' / filename
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:  # read list of expected column names
            lines = f.readlines()
            sheets = [line.strip().split(';')[0] for line in lines]
            fields = [line.strip().split(';')[1] for line in lines]
            for index, s in enumerate(sheets):
                if s == sheet:
                    df_field_names = get_comparable_names(list(df.columns))
                    etalon = fields[index].split(',')
                    difference = get_fields_diff(df_field_names, etalon)
    except FileNotFoundError as e:
        print(f"but CAN'T find field-names file: {filename} to check fields in sheet:\n error {e}")
    return difference


def check_file_sheet_names(f, sheet_name_originals):
    result = []
    try:
        sheets_in_file = get_sheets(f)
        for sheet in sheets_in_file:
            if sheet not in sheet_name_originals:
                print(f'Alert, unknown sheet "{sheet}" in {f}: ')
                result.append(sheet)
                return 1, result
        return 0, result
    except (ValueError, PermissionError) as e:
        print(f'File is open, unreadable, error: {e}')
        return 2, result


def get_sheets(f):
    try:
        sheets_in_file = pd.read_excel(f, sheet_name=None, header=0)
    except Exception as e:
        print(f'Excel read had produced an error: {e}')
        return {}
    return sheets_in_file


def check_excel_for_sheet_names(libreka_files, expected_sheet_names):
    errored_files = {}
    for f in libreka_files:
        sheets_in_file = get_sheets(f)  # dict sheet_name: df
        sheet_error, errored_sheets = check_file_sheet_names(f, expected_sheet_names)
        if sheet_error == 0 and len(errored_sheets) == 0:
            print(f'Sheets are as expected in file {f}')
        elif sheet_error == 1:
            print(f"There's some weird shit going on in {f}, unknown sheet in file.\n{sheets_in_file.keys()}")
            errored_files[f.name] = errored_sheets
        elif sheet_error == 2:
            print('File read error, signing off...')
            errored_files[f.name] = errored_sheets
    return errored_files


def check_field_anomalies(f):
    result = []
    err_sheets = []
    sheets = get_sheets(f)  # dict

    for sheet, df in sheets.items():
        err_fields = check_sheet_df(sheet, df)  # check fields in sheet
        if len(err_fields) > 0:
            print(f"\nERROR!!! Columns in file `{f.name}`, sheet `{sheet}` NOT matching the expected.")
            err_sheets.append(sheet)
            result.append(err_fields)
    if len(err_sheets) > 0:
        return {f.name: err_sheets}, result
    else:
        return {}, []


def main(dirpath):
    p = Path(dirpath)
    expected_sheet_names = ('E-Book-Verkäufe', 'Hörbuch-Verkäufe', 'Kostenlostitel', 'Abo und Flatrate')
    libreka_excel_files = [item for item in p.iterdir() if item.is_file() and item.suffix == '.xlsx'
                           and item.name[:2] != '~$']  # list
    good_for_table_names = get_table_names(expected_sheet_names)  # dict

    # check sheet names in file
    sheet_errors = check_excel_for_sheet_names(libreka_excel_files, expected_sheet_names)  # dict
    if sheet_errors:
        print(f'\nSheet summary: sheet names are off here - {sheet_errors}\n')

    # check errors in field names
    field_errors = []
    for f in libreka_excel_files:
        errored_fields_in_file, extra_fields = check_field_anomalies(f)  # send to examine file
        if errored_fields_in_file:
            field_errors.append((errored_fields_in_file, extra_fields))
    if field_errors:
        print('\nFields summary: field names are off - ', field_errors)

    # actual db write
    if len(sheet_errors) == 0 and len(field_errors) == 0:
        for f in libreka_excel_files:
            sheets_in_file = get_sheets(f)
            for sheet, df in sheets_in_file.items():
                table_name = 'libreka_' + good_for_table_names.get(sheet, "no_name")
                sql_writer.write_to_db(df, table_name, 'append', '19')  # select DB, here: 19
    else:
        print('\nDB write is a no-go. Fix the source files first.')


if __name__ == '__main__':
    # main('/Users/frank/pd/sales_report/16_libreka')
    main('k:/PD/data/sales_report/16_libreka')
