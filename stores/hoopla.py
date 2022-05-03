from pathlib import Path

import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE = 'stg_fin2_41_hoopla'
FILENAME = '-Publish Drive Reporting'
DATA_DIR = 'hoopla'
SUM_FIELD = 'Royalty Due'


def hoopla(hova=HOVA):
    res = []
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
                try:
                    df.drop(df[df['Transaction ID'] == 'Grand Total'].index, inplace=True)
                except KeyError as e:
                    print(f"No drop field")
                    df.drop(df[df['ISBN'] == ''].index, inplace=True)
                szumma = df[SUM_FIELD].sum()
                record_count = df.shape[0]
                sqw.write_to_db(df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    hoopla(hova='pd')


if __name__ == '__main__':
    main()
