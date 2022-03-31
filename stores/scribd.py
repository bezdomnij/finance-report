from pathlib import Path
import warnings
import pandas as pd
from engineer import sql_writer as sqw

FILENAME_1 = 'PublishDrive_scribd_subscriptions_payouts_'
FILENAME_2 = 'PublishDrive2_scribd_subscriptions_payouts_'
TABLE = 'stg_fin2_19_scribd'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'scribd'
SUM_FIELD = 'Amount owed for this interaction'


def scribd(dirpath, hova='0'):
    all_df = pd.DataFrame()
    szumma = 0
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    record_count = 0
    for f in p.iterdir():
        if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls' or f.suffix == '.XLS') and (
                FILENAME_1 in f.stem or FILENAME_2 in f.stem) and f.stem[:2] != '~$':
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(f, header=0, index_col=None)
            if df.shape[0] > 0:
                record_count += df.shape[0]
                szumma += df[SUM_FIELD].sum()
                all_df = all_df.append(df)
                print(f'file: {f.stem}, {df.shape[0]} records, {szumma:-10,.3f}')

    print(f'{record_count} total records')
    szumma = all_df[SUM_FIELD].sum()
    print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}\n")
    sqw.write_to_db(all_df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)


if __name__ == '__main__':
    scribd('/Users/frank/pd/Nextcloud', hova='0')
    # overdrive_audio('h:/NextCloud/Operative/Admin dev/live_sales_v2')
