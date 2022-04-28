from pathlib import Path

import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_20101_findaway_'
FILENAME = 'Digital Royalty)'
DATA_DIR = 'findaway'
SUM_FIELD = 'Royalty Payable'


def findaway(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    record_count = 0
    print(p)
    if files:
        for f in files:
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
                sheet_names = ['Library', 'Retail', 'Subscription', 'Pool']
                for s in sheet_names:
                    df = pd.read_excel(f, sheet_name=s, header=0)
                    print(f"{df[SUM_FIELD].sum():-10.2f} {s}, records: {df.shape[0]}")
                    record_count += df.shape[0]
                    table = TABLE + s.lower()
                    sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')
                print(record_count)


def main():
    findaway(hova='19')


if __name__ == '__main__':
    main()
