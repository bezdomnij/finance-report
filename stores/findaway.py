import re
from datetime import date
from pathlib import Path

import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_fin2_20101_findaway_'
FILENAME = 'Digital Royalty)'
DATA_DIR = 'findaway'
SUM_FIELD = 'Royalty Payable'


def get_dates_from_filename(stem):
    year, month = 0, 0
    pattern = r'\(202[0-9]-([0][0-9]|[1][0-2]) Digital Royalty\)'
    p = re.compile(pattern)
    result = re.search(p, stem)
    result = result.group(0)
    pattern2 = r'202[0-9]-([0][1-9]|[1][0-2])'
    p2 = re.compile(pattern2)
    ym = re.search(p2, result)
    y, m = ym.group(0).split('-')
    try:
        year = int(y)
        month = int(m)
    except Exception as e:
        print(f"{e}: no conversion to int")
    last_day = util.MAX_DAYS[month]
    # print(y, m, last_day)
    return date(year, month, 1), date(year, month, last_day)


def findaway(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    record_count = 0
    if files is None:
        return
    if len(files) > 0:
        print(p)
        for f in files:
            szumma = 0
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
                dates = get_dates_from_filename(f.stem)
                print(dates)
                sheet_names = ['Library', 'Retail', 'Subscription', 'Pool']
                for s in sheet_names:
                    try:
                        df = pd.read_excel(f, sheet_name=s, header=0)
                    except ValueError as e:
                        print(f"{s} sheet is not there!")
                        continue
                    szm = round(df[SUM_FIELD].sum(), 3)
                    print(f"{szm:-10.2f} {s}, records: {df.shape[0]}")
                    rc = df.shape[0]
                    res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc,
                                      'USD', s, szm, dates[0], dates[1]))
                    szumma += szm
                    record_count += rc
                    table = TABLE + s.lower()
                    sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total {szumma:10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    findaway(hova='19')


if __name__ == '__main__':
    main()
