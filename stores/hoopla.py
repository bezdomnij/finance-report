from pathlib import Path

import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_41_hoopla'
FILENAME = '-Publish Drive Reporting'
DATA_DIR = 'hoopla'
SUM_FIELD = 'Royalty Due'


def hoopla(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.suffix in ('.xls', '.xlsx', '.XLS') and FILENAME in f.stem and f.stem[:2] != '~$':
                df = pd.read_excel(f, header=0, index_col=None)
                new_cols = [col.strip() for col in df.columns]
                cols_map = dict(zip(df.columns, new_cols))
                df.rename(columns=cols_map, inplace=True)
                df.drop(df[df['Transaction ID'] == 'Grand Total'].index, inplace=True)
                szumma = df[SUM_FIELD].sum()
                record_count = df.shape[0]
                sqw.write_to_db(df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, total: {szumma:-10,.2f}\t{record_count:10,d} records\n")
    else:
        print(f"Looks like the `{DATA_DIR}` directory is empty.")


def main():
    hoopla(hova='19')


if __name__ == '__main__':
    main()
