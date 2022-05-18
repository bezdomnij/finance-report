from pathlib import Path
import warnings
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

FILENAME_1 = 'PublishDrive_scribd_subscriptions_payouts_'
FILENAME_2 = 'PublishDrive2_scribd_subscriptions_payouts_'
TABLE = 'stg_fin2_19_scribd'
DATA_DIR = 'scribd'
SUM_FIELD = 'Amount owed for this interaction'
DATE_FIELD = 'Threshold Date'


def scribd(hova=HOVA):
    res = []
    all_df = pd.DataFrame()
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    szumma = 0
    record_count = 0
    if len(files) > 0:
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
                    print(f'file: {f.stem}, {rc:10d} records, total: {szm:10,.3f}')
                    res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc, 'USD', '', szm))
                    record_count += rc
                    szumma += szm

        date_borders = util.get_df_dates(DATE_FIELD, 1, all_df)
        print(date_borders)
        szumma = all_df[SUM_FIELD].sum()
        sqw.write_to_db(all_df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10d} records, total: {szumma:-10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    scribd(hova='19')


if __name__ == '__main__':
    main()
