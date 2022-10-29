from pathlib import Path
import pandas as pd
import util
from config import MAIN_DIR, HOVA, REPORT_MONTH
from result import Result

TABLE = 'stg_fin2_42_Dreame_Q'
FILENAME = 'PublishDrive-Sales Report-2022.Q'

# **************** #  +1 month or +2 months or ZERO (quarterly it's 0)
# REPORT_MONTH = '2022_03_march'
# **************** #

DATA_DIR = 'dreame'
SUM_FIELD = 'Royalties(US$)'


def dreame_month(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)

    # disable chained assignments
    pd.options.mode.chained_assignment = None
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.suffix in ('.xls', '.XLS', '.xlsx') and FILENAME in f.stem and f.stem[:2] != '~$':
                record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'CP Book ID', 1)
                print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
                      f", {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    dreame_month('0')


if __name__ == '__main__':
    main()
