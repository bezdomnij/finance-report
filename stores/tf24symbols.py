from datetime import datetime
from pathlib import Path

import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from result import Result

TABLE = 'stg_fin2_28_24symbols'
FILENAME = 'D343_'
DATA_DIR = '24symbols'
SUM_FIELD = 'Income to invoice'


def get_date_from_name(stem):
    dates = []
    parts = stem.split('_')
    for d in parts[1:]:
        dates.append(datetime.strptime(d, '%Y%m%d').date())
    return dates


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
                dates = get_date_from_name(f.stem)
                min_date = dates[0].strftime('%Y-%m-%d')
                max_date = dates[1].strftime('%Y-%m-%d')
                dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                          na_field='', header=5)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-10,.2f}"
                      f" from filename: {min_date}, {max_date}\n")
                res.append(Result(DATA_DIR, REPORT_MONTH, dimensions[0], 'USD', '',
                                  dimensions[1], dates[0], dates[1]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    tfsymbols(hova='pd')


if __name__ == '__main__':
    main()
