from pathlib import Path
import pandas as pd
from util import util

TABLE = 'stg_rts2_35_cnpiec'
FILENAME = '_CNPeReading Sales Report_PublishDrive'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'cnpiec'
SUM_FIELD = 'Net amount to Publisher'


def cnpiec(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    # file, table, hova, sum_field, na_field, header = 0
    for f in p.iterdir():
        if f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
            record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'Order date', header=0)
            print(f"{DATA_DIR}, {REPORT_MONTH}, osszeg: {szumma:-10,.3f}, {record_count} records\n")


def main():
    # cnpiec('/Users/frank/pd/Nextcloud', hova='0')
    cnpiec('h:/Nextcloud/Finance/szamitas', hova='0')


if __name__ == '__main__':
    main()
