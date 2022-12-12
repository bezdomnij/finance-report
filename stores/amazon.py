from pathlib import Path

import pandas as pd

import util
from checker import data_checker
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw
from result import Result

DATA_DIR = 'amazon'
DATE_FIELD = 'Date'
DATE_PRINT_FIELD = 'Sale Date'


def make_df(files, amazon, hova=HOVA):
    result = []
    dates = []
    for f in files:
        marker = 'KEP'
        df = pd.read_excel(f, header=0, index_col=None)
        if ' ' in df.columns:
            df.drop(df.columns[[27]], axis=1, inplace=True)
        too_many_chars = data_checker.d_checker(df=df, right_length=255)
        if too_many_chars:
            print(f'Look out, "{f.name}" has extra lengths: {too_many_chars}')

        szumma = round(df['Payment Amount'].sum(), 3)
        amounts = {}

        if 'KEP_DASH' in f.stem.upper():
            # for BRL currency there is a 15% tax, we do not want to give it to the user, as we don't get it either
            # df updated for BRL only, to 85% of the original amount
            # df is written to sql with reduced by 15% BRL amounts ->
            df.loc[df['Payment Amount Currency'] == 'BRL', 'Payment Amount'] *= 0.85
            currencies = df['Payment Amount Currency'].unique()
            currencies.sort()
            for c in currencies:
                df2 = df[df['Payment Amount Currency'] == c]
                # if c == 'BRL':
                #     print("fukk")
                #     df.loc[df['Payment Amount Currency'] == 'BRL', 'Payment Amount'] *= 0.85  -- ez jo
                #     df.loc[df['Payment Amount Currency'] == c, 'Payment Amount'] *= 0.85
                amounts[c] = []
                amounts[c].append(df2.shape[0])
                amounts[c].append(round(df2['Payment Amount'].sum(), 3))
                print(f"{c}: {amounts[c][1]:-18,.2f}")
            dates = util.get_df_dates(DATE_FIELD, 0, df)
            # print(date_b)

        if 'PRINT_DASH' in f.stem.upper():
            currencies = df['Royalty Amount Currency'].unique()
            marker = 'POD'
            df = df.sort_values(by=['Royalty Amount Currency'])
            currencies.sort()
            for c in currencies:
                df2 = df[df['Royalty Amount Currency'] == c]
                amounts[c] = []
                amounts[c].append(df2.shape[0])
                amounts[c].append(round(df2['Payment Amount'].sum(), 3))
                print(f"{c}: {amounts[c][1]:-18,.2f}")
            dates = util.get_df_dates(DATE_PRINT_FIELD, 0, df)
            print(dates)

        date_borders = dates
        record_count = df.shape[0]
        sqw.write_to_db(df, amazon[f], db_name='stage', action='replace', hova=hova, field_lens='vchall')
        print(f"{DATA_DIR.upper()}_{marker} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
        for k, v in amounts.items():
            # print(k, v)
            result.append(Result(DATA_DIR.upper() + '_' + marker, REPORT_MONTH, v[0], k, '',
                                 v[1], date_borders[0], date_borders[1]))
    return result


def amz_read(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    print(p)
    amazon = {}
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files = [f for f in files if f.suffix == '.xlsx' and f.stem[:2] != '~$']
        if len(files) == 2:
            for item in files:
                if 'kep_print_dashboard' in item.stem or 'amazon_POD' in item.stem:
                    amazon[item] = 'stg_fin2_30666_Amazon_pod'
                elif 'kep_dashboard' in item.stem or 'amazon_KEP' in item.stem:
                    amazon[item] = 'stg_fin2_10666_Amazon_kep'
                else:
                    print(f'Not regular amazon file in here, {item}')
                    return
        else:
            print(f"Directory content not clean, has {len(files)} items.")
            return
        res = make_df(files, amazon, hova)
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    amz_read(hova='pd')
