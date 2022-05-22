"""
able to handle multiple files in report directory
collects dfs and sums in a dictionary - key is sheet name, value is a
list of properties of the type (ebook, sub)
"""

from pathlib import Path

import pandas as pd
from result import Result
import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATA_DIR = 'libreka'
TABLE_EBOOK = 'stg_fin2_16_tolino_libreka_agency'
TABLE_SUB = 'stg_fin2_16_tolino_libreka_subscr'
SUM_FIELD = 'Erlösanteil Geschäftspartner Netto'
DATE_FIELD = 'Datum'


def get_content(df):
    df['Datum'] = pd.to_datetime(df['Datum'], format="%d.%m.%Y").dt.date
    df['month'] = pd.DatetimeIndex(df['Datum']).month
    df.fillna(value='', inplace=True)
    net_income = df[SUM_FIELD].sum()
    rec_count = df.shape[0]
    return df, net_income, rec_count


def libreka(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        sheet_names = ['E-Book-Verkäufe', 'Abo und Flatrate']
        df_collection = dict.fromkeys(sheet_names)

        # init
        for s in sheet_names:
            table = TABLE_EBOOK if s == 'E-Book-Verkäufe' else TABLE_SUB
            df_collection[s] = []
            df_collection[s].append(table)
            df_collection[s].append(pd.DataFrame())
            df_collection[s].append(0)
            df_collection[s].append(0)

        for f in files:
            if f.suffix == '.xlsx' and '5288812' in f.stem and f.stem[:2] != '~$':
                df_dict = pd.read_excel(f, sheet_name=None, header=0)
                for s in sheet_names:
                    df = df_dict.get(s, pd.DataFrame())
                    df, szumma, rc = get_content(df)
                    df_collection[s][1] = df_collection[s][1].append(df, ignore_index=True)
                    df_collection[s][2] += szumma
                    df_collection[s][3] += rc
                    min_date = df_collection[s][1]['Datum'].min()
                    print(s, 'min', min_date)
                    max_date = df_collection[s][1]['Datum'].max()
                    print(s, 'max', max_date)
                    df_collection[s].append(min_date)
                    df_collection[s].append(max_date)
                    print(f"{s} min.Date: {df_collection[s][1]['Datum'].min()} EEEES {df_collection[s][4]}| "
                          f"max.Date: {df_collection[s][1]['Datum'].max()} EEEES {df_collection[s][5]}")

        for k, v in df_collection.items():
            sqw.write_to_db(v[1], v[0], field_lens='vchall', hova=hova, action='replace')
            print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {v[0]}, {v[3]} records, total: {v[2]:10,.2f}\n")
            res.append(Result(DATA_DIR.upper(), REPORT_MONTH, v[3],
                              'EUR', '', v[2], v[4], v[5]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    libreka(hova='19')


if __name__ == '__main__':
    main()
