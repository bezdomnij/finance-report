from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
import util

TABLE = 'stg_fin2_28_24symbols_data'
FILENAME = 'D343_'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = '24symbols'
SUM_FIELD = 'Income to invoice'


def tfsymbols(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    for f in p.iterdir():
        if f.suffix == '.xlsx' and FILENAME in f.stem and f.name[:2] != '~$':
            dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                      na_field='', header=5)
            print(f"{DATA_DIR} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-10,.3f}\n")


def main():
    tfsymbols('/Users/frank/pd/Nextcloud', '0')
    # dreane_month('e:/pd/sales_report', '0')


if __name__ == '__main__':
    main()
