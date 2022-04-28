from pathlib import Path
import warnings
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH

FILENAME_1 = 'PublishDrive_scribd_subscriptions_payouts_'
FILENAME_2 = 'PublishDrive2_scribd_subscriptions_payouts_'
TABLE = 'stg_fin2_19_scribd'
DATA_DIR = 'scribd'
SUM_FIELD = 'Amount owed for this interaction'


def scribd(hova='0'):
    all_df = pd.DataFrame()
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    szumma = 0
    record_count = 0
    if files:
        for f in files:
            if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls' or f.suffix == '.XLS') and (
                    FILENAME_1 in f.stem or FILENAME_2 in f.stem) and f.stem[:2] != '~$':
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("always")
                    df = pd.read_excel(f, header=0, index_col=None)
                if df.shape[0] > 0:
                    rc = df.shape[0]
                    szm = df[SUM_FIELD].sum()
                    all_df = all_df.append(df)
                    print(f'file: {f.stem}, {rc:10d} records, {szm:10,.3f}')
                    record_count += rc
                    szumma += szm

    szumma = all_df[SUM_FIELD].sum()
    print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.2f} | {record_count:10d} total record count\n")
    sqw.write_to_db(all_df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)


def main():
    scribd(hova='19')


if __name__ == '__main__':
    main()
