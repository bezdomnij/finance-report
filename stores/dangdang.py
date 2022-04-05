from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

TABLE = 'stg_fin2_38_dangdang'
FILENAME = 'Order_Dangdang_PublishDrive_'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'dangdang'
SUM_FIELD = 'Payment Amount'


def dangdang(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    # file, table, hova, sum_field, na_field, header = 0
    for f in p.iterdir():
        if f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
            df = pd.read_excel(f, header=7, index_col=None)
            new_cols = [col.strip() for col in df.columns]
            cols_map = dict(zip(df.columns, new_cols))
            df.rename(columns=cols_map, inplace=True)
            df = df[df['Title'].notna()]
            record_count = df.shape[0]
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, osszeg: {szumma:-10,.2f}, {record_count} records\n")
            sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')


def main():
    dangdang('/Users/frank/pd/Nextcloud/szamitas', hova='0')
    # dangdang('h:/Nextcloud/Finance/szamitas', hova='0')


if __name__ == '__main__':
    main()
