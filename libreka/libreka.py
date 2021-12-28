import re
import sys
from pathlib import Path
import pandas as pd
from engineer import sql_writer


def get_comparable_names(columns):
    prog = re.compile(r"\.[0-9]$")
    for index, col in enumerate(columns):
        z = re.search(prog, col)
        if z:
            columns[index] = col[:-2]
    return columns


def check_sheet_df(sheet, df):
    error = 0
    with open('sheet_field.txt', mode='r') as f:
        lines = f.readlines()
        sheets = [line.strip().split(';')[0] for line in lines]
        fields = [line.strip().split(';')[1] for line in lines]
        for index, s in enumerate(sheets):
            if s == sheet:
                comparable_field_names = get_comparable_names(list(df.columns))
                if not (fields[index].split(',') == comparable_field_names):
                    error = 1
                    break
    return error


def check_file_content(f):
    error = False
    sheet_name_originals = ('E-Book-Verkäufe', 'Hörbuch-Verkäufe', 'Kostenlostitel', 'Abo und Flatrate')
    tables = ('e_book', 'a_book', 'free', 'sub')
    good_names = dict(zip(sheet_name_originals, tables))
    try:
        sheets_in_file = pd.read_excel(f, sheet_name=None, header=0)
        for sheet in sheets_in_file:
            if sheet not in sheet_name_originals:
                print(f'Alert, unknown sheet in {f}, this one: {sheet}')
                error = True
                break
        if not error:
            print(f'Sheets are as expected in file {f}')
            for sheet, df in sheets_in_file.items():
                table_name = 'libreka_' + good_names[sheet]
                field_error = check_sheet_df(sheet, df)
                if field_error:
                    print(f"\nERROR!!! \nColumns in file `{f.name}`, sheet `{sheet}` NOT matching the expected.")
                    print('not going to write it to db. Signing off...')
                    sys.exit(1)
                print(table_name)
                sql_writer.write_to_db(df, table_name, 'append', '19')
        else:
            print(f"There's some weird shit going on in {f}, unknown sheet in file.")
    except ValueError as e:
        print(f'File is open OR not Excel, error: {e}')
    finally:
        print(f'operation on file {f} is finished')


def main(dirpath):
    p = Path(dirpath)
    excel_files = [item for item in p.iterdir() if item.is_file() and item.suffix == '.xlsx']
    for f in excel_files:
        check_file_content(f)


if __name__ == '__main__':
    main('/Users/frank/pd/sales_report/16_libreka')
