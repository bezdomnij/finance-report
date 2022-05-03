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

TABLE_1 = 'stg_fin2_32_bookmate_revshare'
TABLE_2 = 'stg_fin2_32_bookmate_subscr'
FILENAME_1 = 'REVSHARE (Content 2 Connect)'
FILENAME_2 = 'PublishDrive (Content 2 Connect)'
SOURCE_DIR = '2022_08_aug'
DATA_DIR = 'bookmate'
SUM_FIELD = 'Revenue'


# file, table, hova, sumfield, nafield, header=0

def bookmate(hova=HOVA):
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
                    r1, s1 = util.get_content_xl_onesheet(f, TABLE_1, hova, SUM_FIELD, 'User ID', 8)
                if FILENAME_2 in f.stem:
                    r2, s2 = util.get_content_xl_onesheet(f, TABLE_2, hova, SUM_FIELD, 'User ID', 10)
                record1_count += r1
                record2_count += r2
                szumma1 += s1
                szumma2 += s2
        res.append(Result(DATA_DIR.upper() + '1', REPORT_MONTH, record1_count, 'USD', '', szumma1))
        res.append(Result(DATA_DIR.upper() + '2', REPORT_MONTH, record2_count, 'USD', '', szumma2))
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record1_count} records, total: {szumma1:-10,.3f}\n")
        print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record2_count} recordstotal: {szumma2:-10,.3f}\n")
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    bookmate(hova='0')
