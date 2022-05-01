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
    if files is None:
        return
    if len(files) > 0:
        print(p)
        for f in files:
            szumma = 0
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
                sheet_names = ['Library', 'Retail', 'Subscription', 'Pool']
                for s in sheet_names:
                    try:
                        df = pd.read_excel(f, sheet_name=s, header=0)
                    except ValueError as e:
                        print(f"{s} sheet is not there!")
                        continue
                    szm = df[SUM_FIELD].sum()
                    print(f"{szm:-10.2f} {s}, records: {df.shape[0]}")
                    szumma += szm
                    record_count += df.shape[0]
                    table = TABLE + s.lower()
                    sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total {szumma:10,.2f}\n")
    else:
        util.empty(DATA_DIR)


def main():
    findaway(hova='19')


if __name__ == '__main__':
    main()
