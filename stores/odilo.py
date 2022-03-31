"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location identical
- sum field identical: FIELD
- need to drop rows below data
"""

from pathlib import Path
import util

TABLE_1 = 'stg_fin2_33_odilo_ppu'
TABLE_2 = 'stg_fin2_33_odilo_agency'
FILENAME_1 = 'RE_February_2022_PublishDrive_PPU_Sales_Report'
FILENAME_2 = 'RE_February_2022_PublishDrive_Sales_Report'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'odilo'
SUM_FIELD = 'Totals'


def odilo(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0

    for f in p.iterdir():
        r, s = 0, 0
        if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls') and f.stem[:2] != '~$':
            if FILENAME_1 in f.stem:
                r, s = util.get_content_xl_onesheet(f, TABLE_1, hova, SUM_FIELD, 'Title', 1)
            if FILENAME_2 in f.stem:
                r, s = util.get_content_xl_onesheet(f, TABLE_2, hova, SUM_FIELD, 'Title', 1)
            record_count += r
            szumma += s

    print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.2f}, {record_count} records\n")


def main():
    odilo('/Users/frank/pd/Nextcloud/szamitas', hova='0')
    # odilo('h:/Nextcloud/Finance/szamitas', hova='0')


if __name__ == '__main__':
    main()
