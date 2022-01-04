from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


def dibook(dirpath, hova):
    p = Path(dirpath).joinpath('dibook')
    table_name = 'stg_fin2_15_dibook_v2'
    for f in p.iterdir():
        if f.name == 'dibook.xls':
            df = pd.read_excel(f, header=0, index_col=None, sheet_name='Sheet')
            print("elotte", df.shape[0])
            if df['ISBN'].isnull().values.any():
                print("drop!!!!!!")
                df.drop(df.tail(1).index, inplace=True)
            print("utana", df.shape[0])
            sqw.write_to_db(df, table_name, action='replace', field_lens='mas', hova=hova)


if __name__ == '__main__':
    dibook('/Users/frank/pd/finance_report', hova='19')
