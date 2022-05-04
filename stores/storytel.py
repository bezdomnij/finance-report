"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location identical
- sum field identical: FIELD
- need to drop rows below data
"""

from pathlib import Path
import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE_1 = 'stg_fin2_43_storytel'
TABLE_2 = 'stg_fin2_20043_storytel_audio'
FILENAME = '_publishdrive-inc_794'
# REPORT_MONTH = '2022_03_march'  # quarterly reporting, approximate month
DATA_DIR = 'storytel'
SUM_FIELD = 'Remuneration (USD)'


def storytel(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls') \
                    and f.stem[:2] != '~$' and FILENAME in f.stem:
                rc, szm = 0, 0
                for sheet in ['A-books', 'E-books']:
                    if sheet == 'A-books':
                        rc, szm = util.get_content_xl_onesheet(f, TABLE_2, hova, SUM_FIELD, '', sheet_name=sheet)
                        print(f"{DATA_DIR.upper() + '_AUDIO'} | {REPORT_MONTH}, "
                              f"{rc} records, total: {szm:-10,.2f}\n")
                        res.append(Result(DATA_DIR.upper() + '_AUDIO', REPORT_MONTH, rc, 'USD', '', szm))
                    if sheet == 'E-books':
                        rc, szm = util.get_content_xl_onesheet(f, TABLE_1, hova, SUM_FIELD, '', sheet_name=sheet)
                        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {rc} records, total: {szm:-10,.2f}\n")
                        res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc, 'USD', '', szm))
                    record_count += rc
                    szumma += szm
        # print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
    else:
        util.empty(DATA_DIR)

    return res


if __name__ == '__main__':
    storytel(hova='19')
