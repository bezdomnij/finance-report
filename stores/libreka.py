from pathlib import Path
from engineer import sql_writer as sqw
import pandas as pd
import numpy as np

DATA_DIR = 'libreka'
REPORT_MONTH = '2022_02_february'
TABLE_EBOOK = 'stg_fin2_16_tolino_libreka_agency'
TABLE_SUB = 'stg_fin2_16_tolino_libreka_subscr'


def libreka(dirpath, hova='0'):
    sheet_names = ['E-Book-Verkäufe', 'Hörbuch-Verkäufe', 'Kostenlostitel', 'Abo und Flatrate']
    df_dict = {}
    libreka_all_ebook = pd.DataFrame()
    libreka_all_sub = pd.DataFrame()
    p = Path(dirpath).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    ebook_sum, sub_sum = 0, 0
    for f in p.iterdir():
        if f.suffix == '.xlsx' and '5288812' in f.stem and f.stem[:2] != '~$':
            try:
                df_dict = pd.read_excel(f, sheet_name=None, header=0)
            except ValueError as e:
                print(f'Excel is open? {e}, {f.stem}')
            df_ebook = df_dict.get(sheet_names[0], pd.DataFrame())
            df_sub = df_dict.get(sheet_names[-1], pd.DataFrame())

            ebook_net_inc = df_ebook['Erlösanteil Geschäftspartner Netto'].sum()
            ebook_sum += ebook_net_inc
            sub_net_inc = df_sub['Erlösanteil Geschäftspartner Netto'].sum()
            sub_sum += sub_net_inc

            df_ebook['Datum'] = pd.to_datetime(df_ebook['Datum'], format="%d.%m.%Y").dt.date
            df_ebook['month'] = pd.DatetimeIndex(df_ebook['Datum']).month
            df_sub['Datum'] = pd.to_datetime(df_sub['Datum'], format="%d.%m.%Y").dt.date
            df_sub['month'] = pd.DatetimeIndex(df_sub['Datum']).month

            df_ebook = df_ebook.where(df_ebook.notna(), '')
            df_sub.fillna(value='', inplace=True)

            print(f"ebook - {f.stem[-6:]}: {ebook_net_inc:12,.2f}, {df_ebook['Datum'].min()}, "
                  f"{df_ebook['Datum'].max()}, - {f.stem[-2:]}, {df_ebook.shape[0]}, {df_ebook.groupby(['month']).size()}")
            print(f"sub   - {f.stem[-6:]}: {sub_net_inc:12,.2f}, {df_sub['Datum'].min()}, "
                  f"{df_sub['Datum'].max()}, - {f.stem[-2:]}, {df_sub.shape[0]}, {df_sub.groupby(['month']).size()}")

            libreka_all_ebook = libreka_all_ebook.append(df_ebook, ignore_index=True)
            libreka_all_sub = libreka_all_sub.append(df_sub, ignore_index=True)

    print(libreka_all_ebook['Datum'].min(), libreka_all_ebook['Datum'].max())
    print(libreka_all_sub['Datum'].min(), libreka_all_sub['Datum'].max())

    print(f"ebooks: {ebook_sum:8,.2f}; subs: {sub_sum:8.2f}; sumsum: {ebook_sum + sub_sum:8,.2f}")
    sqw.write_to_db(libreka_all_sub, TABLE_SUB, field_lens='vchall', hova=hova, action='replace')
    sqw.write_to_db(libreka_all_ebook, TABLE_EBOOK, field_lens='vchall', hova=hova, action='replace')


def main():
    # main('/Users/frank/pd/sales_report', hova='0')
    libreka('h:/NextCloud/Finance/szamitas', hova='19')


if __name__ == '__main__':
    main()
