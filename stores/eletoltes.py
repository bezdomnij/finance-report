"""
multiple sources - two Excels, each file with one sheet only
have to drop the total line
"""
from datetime import datetime
from pathlib import Path
import re
import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_fin2_18_eletoltes'
FILENAME = 'letoltheto_riport_C2C_2022febr'
DATA_DIR = 'eletoltes'
SUM_FIELD = 'Content 2  Connect részesedés (nettó)'
FILE_MONTH = {
    'jul': '07',
    'jun': '06',
    'maj': '05',
    'apr': '04',
    'marc': '03',
    'febr': '02',
}


def get_files(stem):
    year, month = None, None
    parts = stem.split('_')
    print(parts[-1])
    pattern = r"(202[0-9])(\w{3})$"
    p = re.compile(pattern)
    m = re.match(p, parts[-1])
    if m:
        year = m.group(1)
        month = FILE_MONTH[m.group(2)]
    return '-'.join([year, month, '15'])


def eletoltes(hova=HOVA):
    """
    collects data from multiple files and lumps them to db
    dropping empty: (1) convert '' to np.nan, (2) drop rows where nan
    :param hova: locally can be different from global
    :return: Result object
    """
    res = []
    dates = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0
    print(p)
    files = util.get_file_list(p)
    files = util.get_latest_files(files, 2)
    df_all = pd.DataFrame()
    if files is None:
        return
    if len(files) > 0:

        for f in files:
            if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls') and f.stem[:2] != '~$':
                date = get_files(f.stem)
                date_date = datetime.strptime(date, '%Y-%m-%d').date()
                dates.append(date_date)
                df = pd.read_excel(f, header=0, index_col=None)
                # df['ISBN szám'].replace('', np.nan, inplace=True)  # convert '' to nan
                df['ISBN szám'].astype(bool)  # this is the other method: falsy, ez is jo to drop
                df.dropna(subset=['ISBN szám'], inplace=True)  # drop rows where any col is nan
                df['Date'] = date
                rc = df.shape[0]
                szm = df[SUM_FIELD].sum()
                print(f"file: {f.stem}, {rc:10,d} records,\ttotal in file: {szm:-10,.2f}")
                record_count += rc
                szumma += szm
                df_all = df_all.append(df)

        sqw.write_to_db(df_all, TABLE, hova=hova, field_lens='vchall')
        print(dates)
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
        res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'HUF', '', szumma, min(dates), max(dates)))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    eletoltes(hova='19')


if __name__ == '__main__':
    main()
