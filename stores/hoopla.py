from pathlib import Path
from engineer import sql_writer as sqw
import pandas as pd

TABLE = 'stg_fin2_41_hoopla'
FILENAME = '-Publish Drive Reporting'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'hoopla'
SUM_FIELD = 'Royalty Due'


def hoopla(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    for f in p.iterdir():
        if f.is_file() and f.suffix in ('.xls', '.xlsx', '.XLS') and FILENAME in f.stem and f.stem[:2] != '~$':
            df = pd.read_excel(f, header=0, index_col=None)
            new_cols = [col.strip() for col in df.columns]
            cols_map = dict(zip(df.columns, new_cols))
            df.rename(columns=cols_map, inplace=True)
            df.drop(df[df['Transaction ID'] == 'Grand Total'].index, inplace=True)
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.2f}\n")
            sqw.write_to_db(df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)


def main():
    # hoopla('h:/Nextcloud/Finance/szamitas', hova='0')
    hoopla('/Users/frank/pd/Nextcloud/szamitas', hova='19')


if __name__ == '__main__':
    main()
