from pathlib import Path
import pandas as pd
from util import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE = 'stg_fin2_22_ciando'
FILENAME = 'Content_2_Connect_71290'
DATA_DIR = 'ciando'
SUM_FIELD = 'Total publisher'


def ciando(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    files = util.get_file_list(p)
    pd.options.mode.chained_assignment = None
    # file, table, hova, sum_field, na_field, header = 0
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
                pass
                record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'Data convers', header=0)
                print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'EUR', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    ciando(hova='0')


if __name__ == '__main__':
    main()
