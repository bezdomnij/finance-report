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

TABLE_1 = 'stg_fin2_32_bookmate_revshare'
TABLE_2 = 'stg_fin2_32_bookmate_subscr'
FILENAME_1 = 'REVSHARE (Content 2 Connect)'
FILENAME_2 = 'PublishDrive (Content 2 Connect)'
SOURCE_DIR = '2022_08_aug'
DATA_DIR = 'bookmate'
SUM_FIELD = 'Revenue'


# file, table, hova, sumfield, nafield, header=0

def bookmate(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0

    for f in p.iterdir():
        r, s = 0, 0
        if f.is_file() and f.suffix == '.xlsx':
            if FILENAME_1 in f.stem:
                r, s = util.get_content_xl_onesheet(f, TABLE_1, hova, SUM_FIELD, 'User ID', 8)
            if FILENAME_2 in f.stem:
                r, s = util.get_content_xl_onesheet(f, TABLE_2, hova, SUM_FIELD, 'User ID', 10)
            record_count += r
            szumma += s

    print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}, {record_count} records\n")


if __name__ == '__main__':
    bookmate(hova='0')
