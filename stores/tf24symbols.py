from pathlib import Path

import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from result import Result

TABLE = 'stg_fin2_28_24symbols_data'
FILENAME = 'D343_'
DATA_DIR = '24symbols'
SUM_FIELD = 'Income to invoice'


def tfsymbols(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.suffix == '.xlsx' and FILENAME in f.stem and f.name[:2] != '~$':
                dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                          na_field='', header=5)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-10,.2f}")
                res.append(Result(DATA_DIR, REPORT_MONTH, dimensions[0], 'USD', dimensions[1]))

    else:
        util.empty(DATA_DIR)
    return res


def main():
    tfsymbols(hova='0')


if __name__ == '__main__':
    main()
