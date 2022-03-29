from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw

TABLE = 'stg_fin2_15_dibook_v2'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'dibook'
FILENAME = 'Elszámolás'


def dibook(dirpath, hova='0'):
    p = Path(dirpath).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    for f in p.iterdir():
        if f.is_file() and FILENAME in f.stem and f.suffix in ['.xls', '.xlsx']:
            df = pd.read_excel(f, header=0, index_col=None, sheet_name='Sheet')
            print("elotte", df.shape[0])
            if df['ISBN'].isnull().values.any():
                print("drop!!!!!!")
                df.drop(df.tail(1).index, inplace=True)
            print("utana", df.shape[0])
            print(df['Beszállító árbevétel összeg nettó'].sum())
            sqw.write_to_db(df, TABLE, action='replace', field_lens='mas', hova=hova)


if __name__ == '__main__':
    # dibook('/Users/frank/pd/finance_report/2022_01_january', hova='0')
    dibook('h:/Nextcloud/Finance/szamitas', hova='0')
