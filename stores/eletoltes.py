"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location identical
- sum field identical: FIELD
- need to drop rows below data
"""

from pathlib import Path

import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE = 'stg_fin2_18_eletoltes'
FILENAME = 'letoltheto_riport_C2C_2022febr'
DATA_DIR = 'eletoltes'
SUM_FIELD = 'Content 2  Connect részesedés (nettó)'


# SUM_FIELD = 'Totals'  # valamelyik


def eletoltes(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0
    print(p)
    files = util.get_file_list(p)
    df_all = pd.DataFrame()
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            print(f)
            rc, szm = 0, 0
            if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls') and f.stem[:2] != '~$':
                df = pd.read_excel(f, header=0, index_col=None)
                df.drop(df[df['ISBN szám'] == ''].index, inplace=True)
                df.drop(df.tail(1).index, inplace=True)
                rc = df.shape[0]
                szm = df[SUM_FIELD].sum()
                print(f.stem, rc, szm)
                record_count += rc
                szumma += szm
                df_all = df_all.append(df)

        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
        res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'HUF', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    eletoltes(hova='0')


if __name__ == '__main__':
    main()
