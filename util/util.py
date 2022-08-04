import logging
import re
import warnings
from datetime import datetime
import pandas as pd

from engineer import sql_writer as sqw
from pathlib import Path

DATE_FORMAT = {
    0: '%Y-%m-%d',
    1: '%m/%d/%Y',
    2: '%d/%m/%Y',
    3: '%m/%d/%y',
    4: '%Y. %m. %d.',
    5: '%Y.%m.%d',
    6: '%Y%m%d',
}

MAX_DAYS = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def get_period(fname):
    g_pattern = r'202[0-2]-[0-1][0-9]'
    prog = re.compile(g_pattern)
    return prog.findall(fname)


def set_date(report_month, offset):
    """
    used first with perlego, where we create the date in the df, because the file does not have it
    however: dtae needs to be backdated by offset number of months (1, usually)
    :param report_month:
    :param offset:
    :return: a year_month string to be used in the file date (by adding 15 to it in the calling function)
    """
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


def get_proper_df(f, sheet_name='Details'):
    """
    to get rid of the spaces around field names
    :param f: pathlib file object
    :param sheet_name:
    :return: return a df where no spaces in field names
    """
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(f, sheet_name=sheet_name, header=0, index_col=None)
    col2 = [col.strip() for col in df.columns]
    renamed_cols = dict(zip(df.columns, col2))
    df2 = df.rename(columns=renamed_cols)
    return df2


def get_latest_files(files, count):
    result = []
    files_modded_when = {}
    files_to_use = [f for f in files if f.stem[:2] != '~$' and f.stem[:2] != '._'
                    and f.is_file() and f.stem[:3] != '.DS']
    if files_to_use:
        try:
            for f in files_to_use:
                modify_time = int(f.stat().st_mtime)
                files_modded_when[modify_time] = f
            if bool(files_modded_when):
                keys = sorted(list(files_modded_when.keys()))
                fs_to_use = keys[-count:]
                for k in fs_to_use:
                    # result = files_modded_when.get(keys[:-count], Path())
                    result.append(files_modded_when.get(k, Path()))
        except IndexError as e:
            print(f"No keys? {e}")
    return result


def get_df_dates(date_field, date_format, df):
    df_temp = pd.DataFrame()
    try:
        df_temp['Datum'] = pd.to_datetime(df[date_field], format=DATE_FORMAT[date_format])
    except ValueError as e:
        print(f"!!! ERROR !!! {e}")
        return '', ''
    else:
        min_date = df_temp['Datum'].min().date()
        max_date = df_temp['Datum'].max().date()
        return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')


def get_content_xl_onesheet(file, table, hova, sum_field, na_field, header=0, sheet_name=''):
    record_count, szumma = 0, 0
    # print(hova)
    if sheet_name == '':
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            df = pd.read_excel(file, header=header, index_col=None)  # , engine='openpyxl')  # ???
    else:
        df = get_proper_df(file, sheet_name=sheet_name)
    if na_field != '':
        try:
            df = df[df[na_field].notna()]
        except KeyError as e:
            print(f"KEY error, {e}, nothing is written.")
            return 0, 0.00
    if not df.empty:
        try:
            szumma = round(df[sum_field].sum(), 3)
        except KeyError as e:
            print(f"!!!ERROR ---{file.name}--- ERROR!!! Fields changed")
            return 0, 0.00
        record_count = df.shape[0]
        # print(df.columns)
    print(
        f"{file.parents[0].stem.lower()} | file: {file.stem},  {record_count} records, total: {round(szumma, 3):9,.2f}")
    sqw.write_to_db(df, table, db_name='stage', action='replace', field_lens='vchall', hova=hova)
    return record_count, szumma


def empty(data_dir):
    print(f"\t\tLooks like the `{data_dir}` directory is empty OR does not exist.\n")


def get_file_list(p):
    try:
        files = [f for f in p.iterdir() if f.stem[:2] != '~$' and f.stem != '._']
    except FileNotFoundError as e:
        print(f'apparenty the `{p.stem}` directory is not there\n{p.name.upper()} - {e}\n')
        return []
    return files


def get_latest_file(files, ftype, count=1):
    """
    based on mod time pathlib files are sorted
    :param count: number of files to return
    :param ftype: file type as udsed in pd
    :param files: list of pathlib file objects
    :return: one file as list (easier on the existing code)
    """
    time_file = {}
    result = []
    files_of_type = [x for x in files if x.suffix.lower() == ftype]
    for f in files_of_type:
        mt = f.stat().st_mtime_ns
        time_file.update({mt: f})
    for k, v in time_file.items():
        print(k, v)
    sorted_lst = sorted(list(time_file.keys()))
    try:
        result.append(time_file[sorted_lst[-count]])
    except IndexError:
        print(f"number of files to return, {count} > {len(files_of_type)}")
    return result


def main():
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    # check_file_name("GoogleEarningsReport_whatever.csv")
    check_google_file_name("GoogleEarningsReport_2021-11.csv")


if __name__ == '__main__':
    main()
