from pathlib import Path
import pandas as pd
import util
from config import MAIN_DIR, REPORT_MONTH

TABLE = 'stg_rts2_42_dreame'
FILENAME = 'PublishDrive-Sales Report-2022.3'

# **************** #  +1 month or +2 months or ZERO (quarterly it's 0)
SOURCE_DIR = '2022_03_march'
# **************** #

DATA_DIR = 'dreame'
SUM_FIELD = 'Royalties (US$)'


def dreame_month(hova='0'):
    p = Path(MAIN_DIR).joinpath(SOURCE_DIR).joinpath(DATA_DIR)

    # disable chained assignments
    pd.options.mode.chained_assignment = None
    files = util.get_file_list(p)

    if files:
        for f in files:
            if f.suffix in ('.xls', '.XLS', '.xlsx') and FILENAME in f.stem and f.stem[:2] != '~$':
                record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'CP Book ID', 1)
                print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
                      f"total: {szumma:-10,.2f}\t, {record_count} records")


def main():
    dreame_month('19')


if __name__ == '__main__':
    main()