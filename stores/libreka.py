from pathlib import Path

import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATA_DIR = 'libreka'
TABLE_EBOOK = 'stg_fin2_16_tolino_libreka_agency'
TABLE_SUB = 'stg_fin2_16_tolino_libreka_subscr'
SUM_FIELD = 'Erlösanteil Geschäftspartner Netto'


def get_content(f, df, s):
    df['Datum'] = pd.to_datetime(df['Datum'], format="%d.%m.%Y").dt.date
    df['month'] = pd.DatetimeIndex(df['Datum']).month
    df.fillna(value='', inplace=True)
    net_income = df[SUM_FIELD].sum()
    print(f"{s} - {f.stem[-6:]}: {net_income:12,.2f}, {df['Datum'].min()}, "
          f"{df['Datum'].max()}, - {f.stem[-2:]}, {df.shape[0]}, "
          f"{df.groupby(['month']).size()}")
    return df, net_income


def libreka(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        sheet_names = ['E-Book-Verkäufe', 'Abo und Flatrate']
        df_collection = {}
        for f in files:
            if f.suffix == '.xlsx' and '5288812' in f.stem and f.stem[:2] != '~$':
                df_dict = pd.read_excel(f, sheet_name=None, header=0)

                for s in sheet_names:  # collect dfs and sums
                    # initialize
                    table = str(s) + '_table'
                    df_collection[s] = []  # pd.DataFrame()
                    df_collection[s].append(pd.DataFrame())
                    df_collection[s].append(0)
                    df_collection[s].append(table)

                    # action on this df
                    df = df_dict.get(s, pd.DataFrame())
                    df, szumma = get_content(f, df, s)
                    df_collection[s][0] = df_collection[s][0].append(df, ignore_index=True)
                    df_collection[s][1] += szumma
                    print(f"{s} min.Date: {df_collection[s][0]['Datum'].min()} | "
                          f"max.Date: {df_collection[s][0]['Datum'].max()}")

        # for k, v in df_collection.items():
        #     print(k, v)
        # sqw.write_to_db(, TABLE_SUB, field_lens='vchall', hova=hova, action='replace')
        # sqw.write_to_db(libreka_all_ebook, TABLE_EBOOK, field_lens='vchall', hova=hova, action='replace')
        # print(f"{DATA_DIR.upper()} | ebooks: {ebook_sum:-10,.2f}; subs: {sub_sum:-10,.2f}; "
        #       f"sumsum: {ebook_sum + sub_sum:-10,.2f}\n")
    else:
        util.empty(DATA_DIR)


def main():
    libreka(hova='19')


if __name__ == '__main__':
    main()
