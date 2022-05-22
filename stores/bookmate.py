"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location varies
- sum field identical: FIELD
- need to drop rows below data
"""

from pathlib import Path
import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result
from datetime import date, datetime

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


def bookmate(hova=HOVA):
    global min1_date, max1_date, min2_date, max2_date
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma1, szumma2 = 0, 0
    record1_count, record2_count = 0, 0
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            r1, s1, r2, s2 = 0, 0, 0, 0
            if f.is_file() and f.suffix == '.xlsx':
                if FILENAME_1 in f.stem:
                    print(hova)
                    min1_date, max1_date = get_dates_from_filename(f.stem)
                    r1, s1 = util.get_content_xl_onesheet(f, TABLE_1, hova, SUM_FIELD, 'User ID', 8)
                if FILENAME_2 in f.stem:
                    min2_date, max2_date = get_dates_from_filename(f.stem)
                    r2, s2 = util.get_content_xl_onesheet(f, TABLE_2, hova, SUM_FIELD, 'User ID', 10)
                record1_count += r1
                record2_count += r2
                szumma1 += s1
                szumma2 += s2
        res.append(Result(DATA_DIR.upper() + '1', REPORT_MONTH, record1_count,
                          'USD', 'revshare', szumma1, min1_date, max1_date))
        res.append(Result(DATA_DIR.upper() + '2', REPORT_MONTH, record2_count,
                          'USD', 'subscr', szumma2, min2_date, max2_date))
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record1_count} records, total: {szumma1:-10,.3f}\n")
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record2_count} recordstotal: {szumma2:-10,.3f}\n")
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    bookmate(hova='19')
