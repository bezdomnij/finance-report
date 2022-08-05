"""
alternate source, because report month and actual content month differ, hence MAIN2_DIR for live sales
this can change if some routine is formed in reporting
"""
from pathlib import Path

import util
from result import Result
from engineer import sql_writer as sqw
from config import HOVA, REPORT_MONTH, MAIN_DIR
import pandas as pd

DATA_DIR = 'baker'
SUM_FIELD = 'Proceeds of sale due to publisher'
TABLE = 'stg_fin2_47_baker'


def baker(hova=HOVA):
    res = []
    df_all = pd.DataFrame()
    record_count, szumma = 0, 0.00
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = [f for f in p.iterdir() if f.suffix == '.xlsx' and f.stem[:2] != '._' and f.stem[:2] != '~$']
    if files:
        if len(files) > 0:
            min_date, max_date = '', ''
            for f in files:
                df = pd.read_excel(f, header=5, index_col=None)
                col2 = [c.replace('\n', '').strip() for c in df.columns]
                renamed_cols = dict(zip(df.columns, col2))
                df2 = df.rename(columns=renamed_cols)
                # df2.info()
                # print(df2['Transaction date or date and time'])
                df2 = df2.iloc[:-1]
                # df2.drop(df2.index[-1], inplace=True)  # that also works
                # df2 = df2.dropna(how='all')
                # df2.drop(df2[df2['Main product ID#'] is None].index, inplace=True)
                rc = df2.shape[0]
                szm = round(df2[SUM_FIELD].sum(), 2)
                print(f"{f.parents[0].stem.lower()} | amount {szm}, {rc} records")
                record_count += rc
                szumma += szm
                df_all = df_all.append(df2, ignore_index=True)
                min_date = df_all['Transaction date or date and time'].min().date()
                max_date = df_all['Transaction date or date and time'].max().date()
            print(f"min. date: {min_date}, \tmax. date: {max_date}")

            sqw.write_to_db(df_all, TABLE, hova=hova, field_lens='vchall')
            print(f"{DATA_DIR.upper()}\treport: {REPORT_MONTH},\ttotal: {szumma:8,.2f},\t{record_count} records\n")
            res.append((Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                               'USD', '', szumma, min_date, max_date)))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    baker(hova='19')


if __name__ == '__main__':
    main()
