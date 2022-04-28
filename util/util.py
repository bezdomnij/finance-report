import logging
import re
import warnings
import pandas as pd
from engineer import sql_writer as sqw
from pathlib import Path


def get_period(fname):
    g_pattern = r'202[0-2]-[0-1][0-9]'
    prog = re.compile(g_pattern)
    return prog.findall(fname)


def set_date(report_month, offset):
    parts = report_month.split('_')
    year, month = int(parts[0]), int(parts[1])
    temp_month = month + offset
    month = month + offset if temp_month != 0 else 12
    year = year if temp_month != 0 else year - 1
    return '_'.join([str(year), str(month).zfill(2)])


def check_google_file_name(fname):
    result = get_period(fname)
    name_and_extension = fname.split('.')
    if 'GoogleEarningsReport' in name_and_extension[0] and name_and_extension[-1] == 'csv':
        name_parts = name_and_extension[0].split('_')  # gg-nel nincs benne _
        period = tuple(get_period(fname)[0].split('-'))
        if len(period) > 0:
            if len(name_parts) == 2:  # ilyen a GoogleAudio
                result = ('ga', period)
            elif len(name_parts) == 1:
                result = ('gg', period)
            else:
                print("Filename is not ok, too many parts (sep='_')")
                return None, period
        else:
            period = (0, 0)
        if period[0] == 0 or period[1] == 0:
            print("Don't know the period of filename.")
            return None, period
    else:
        print("Does not appear to be a Google earnings .csv report.")
    return result


def check_incoming(f):
    ftype, period = check_google_file_name(f.name)
    print(ftype, period)
    return ftype, period


def get_proper_df(f, sheet_name='Details'):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(f, sheet_name=sheet_name, header=0, index_col=None)
    col2 = [col.strip() for col in df.columns]
    renamed_cols = dict(zip(df.columns, col2))
    df2 = df.rename(columns=renamed_cols)
    return df2


def get_content_xl_onesheet(file, table, hova, sum_field, na_field, header=0, sheet_name=''):
    record_count, szumma = 0, 0
    if sheet_name == '':
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            df = pd.read_excel(file, header=header, index_col=None)  # , engine='openpyxl')  # ???
    else:
        df = get_proper_df(file, sheet_name=sheet_name)
    if na_field != '':
        df = df[df[na_field].notna()]
    if not df.empty:
        szumma = df[sum_field].sum()
        record_count = df.shape[0]
        # print(df.columns)
    print(
        f"{file.parents[0].stem.lower()} | file: {file.stem}, osszege: "
        f"{round(szumma, 3):-18,.2f}, {record_count} records")
    sqw.write_to_db(df, table, db_name='stage', action='replace', field_lens='vchall', hova=hova)
    return record_count, szumma


def get_file_list(p):
    try:
        files = [f for f in p.iterdir()]
    except FileNotFoundError as e:
        print(f'apparenty the `{p.stem}` directory is not there\n{p.name.upper()} - {e}\n')
        return None
    return files


def get_path(dirpath, directory):
    return Path(dirpath).joinpath(directory)


def main():
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    # check_file_name("GoogleEarningsReport_whatever.csv")
    check_google_file_name("GoogleEarningsReport_2021-11.csv")


if __name__ == '__main__':
    main()
