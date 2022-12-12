"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location varies
- sum field identical: FIELD
- need to drop rows below data
"""

from pathlib import Path
import util
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result
from datetime import datetime, timedelta
import warnings
from engineer import sql_writer as sqw

TABLE_1 = 'stg_fin2_32_bookmate_revsh'
TABLE_2 = 'stg_fin2_32_bookmate_subs'
FILENAME_1 = 'REVSHARE (Content 2 Connect)'
FILENAME_2 = 'PublishDrive (Content 2 Connect)'
SOURCE_DIR = '2022_08_aug'
DATA_DIR = 'bookmate'
SUM_FIELD = 'Revenue'


# file, table, hova, sumfield, nafield, header=0

def get_dates_from_filename(stem):
    parts = stem.split('_')
    min_date = parts[-2]
    max_date = parts[-1]
    mnd = datetime.strptime(min_date, '%Y-%m-%d').date()
    mxd = datetime.strptime(max_date, '%Y-%m-%d').date()
    return mnd, mxd


def get_content_xl_onesheet(file, sum_field, na_field, header=0, sheet_name=''):
    record_count, szumma = 0, 0
    if sheet_name == '':
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            df = pd.read_excel(file, header=header, index_col=None)  # , engine='openpyxl')  # ???
    else:
        df = util.get_proper_df(file, sheet_name=sheet_name)
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
            print(f"!!!ERROR ---{file.name}--- ERROR!!! Fields changed\n{e}")
            return 0, 0.00
        record_count = df.shape[0]
        # print(df.columns)
    print(
        f"{file.parents[0].stem.lower()} | file: {file.stem},  {record_count} records, total: {round(szumma, 3):9,.2f}")

    return record_count, szumma, df


def bookmate(hova=HOVA):
    df1_all = pd.DataFrame()
    df2_all = pd.DataFrame()
    dates1 = dates2 = []
    # global min1_date, max1_date, min2_date, max2_date
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma1, szumma2 = 0, 0
    record1_count, record2_count = 0, 0
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.suffix == '.xlsx':
                if FILENAME_1 in f.stem:
                    min1_date, max1_date = get_dates_from_filename(f.stem)
                    dates1.append(min1_date)
                    dates1.append(max1_date)
                    r1, s1, df1 = get_content_xl_onesheet(f, SUM_FIELD, 'User ID', 8)
                    # print(df1.columns)
                    df1['Date'] = min1_date + timedelta(days=14)
                    df1['Purchase'] = df1['Purchase'].astype(int)
                    record1_count += r1
                    szumma1 += s1
                    df1_all = df1_all.append(df1)
                    print(df1.shape[0], min1_date, max1_date)
                    # print(df1.tail())
                if FILENAME_2 in f.stem:
                    min2_date, max2_date = get_dates_from_filename(f.stem)
                    dates2.append(min2_date)
                    dates2.append(max2_date)
                    r2, s2, df2 = get_content_xl_onesheet(f, SUM_FIELD, 'User ID', 10)
                    df2['Date'] = min2_date + timedelta(days=14)
                    record2_count += r2
                    szumma2 += s2
                    df2_all = df2_all.append(df2)
                    print(df2.shape[0], min2_date, max2_date)
        res.append(Result(DATA_DIR.upper() + '1', REPORT_MONTH, record1_count,
                          'USD', 'revshare', szumma1, min(dates1), max(dates1)))
        res.append(Result(DATA_DIR.upper() + '2', REPORT_MONTH, record2_count,
                          'USD', 'subscr', szumma2, min(dates2), max(dates2)))
        sqw.write_to_db(df1_all, TABLE_1, db_name='stage', action='replace', field_lens='vchall', hova=hova)
        sqw.write_to_db(df2_all, TABLE_2, db_name='stage', action='replace', field_lens='vchall', hova=hova)
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record1_count} records, total: {szumma1:-10,.3f}")
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record2_count} records, total: {szumma2:-10,.3f}\n")

    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    bookmate(hova='pd')
