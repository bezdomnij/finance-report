"""
NONSTANDARD period - source is NOT the regular monthly report path (MAIN2_DIR), emphasis on 2
source location: network directory live sales
add a date, because the source file does not have it
drop the last line
prepared to handle more than one file, collection df, print file by file
at the end the summary of all content is written to db
The latest file is read from the source directory.
"""
from pathlib import Path

from datetime import datetime
import pandas as pd
from result import Result

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH

TABLE = 'stg_fin2_48_empik'
FILENAME = 'Sprzedaz---Raport-zaawansowany_'
# FILENAME = '_sales report'
SOURCE_DIR = REPORT_MONTH
DATA_DIR = 'empik'
SUM_FIELD = 'Marża wyd. netto'
DATE_FIELD = 'Datum'


def get_date(filename):
    parts = filename.split('_')
    str_datum = parts[-1] + '-15'
    real_datum = datetime.strptime(str_datum, '%Y-%m-%d')
    print(real_datum.date())
    return real_datum.date()


def empik(hova='0'):
    res = []
    p = Path(MAIN_DIR).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # main_dir = '/Volumes/raiddisk/PD/Nextcloud/Operative/Admin dev/live_sales_v2'
    # p = Path(MAIN_DIR).joinpath(DATA_DIR)  # -- sales reporthoz mashol vannak a file-ok
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        df_all = pd.DataFrame()
        record_count, szumma = 0, 0
        latest_files = util.get_latest_files(files, 1)
        print('LATEST:', latest_files[0])
        # files.clear()
        # files.extend(latest_files)
        for f in files:
            if f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$' and f.stem[:2] != '._':
                df = pd.read_excel(f, header=0)
                df = df[df['ISBN'].notna()]
                df['ISBN'] = df['ISBN'].str.replace('-', '')
                rc = df.shape[0]
                szm = df[SUM_FIELD].sum()
                df['Datum'] = get_date(f.stem)
                print(f"{DATA_DIR}, file: {f.stem},\treport: {REPORT_MONTH}, total: {szm:10,.2f}\t, {rc} records")
                record_count += rc
                szumma += szm
                df_all = df_all.append(df)
        date_borders = util.get_df_dates(DATE_FIELD, 0, df_all)
        sqw.write_to_db(df_all, TABLE, action='replace', hova=hova, field_lens='vchall')
        print(f"{DATA_DIR.upper()}, report: {REPORT_MONTH}, total: {round(szumma, 3)}, {record_count} records")
        try:
            res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                              'USD', '', szumma, date_borders[0], date_borders[1]))
        except Exception as e:
            print(f'sg is not right, {e}')
    else:
        util.empty(DATA_DIR)
    return res


def main():
    empik(hova='19')


if __name__ == '__main__':
    main()
