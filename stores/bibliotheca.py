import logging
import warnings
from pathlib import Path
from result import Result
import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATA_DIR = 'bibliotheca'
TABLE = 'stg_fin2_39_bibliotheca'
SUM_FIELD = 'Total proceeds due to publisher'
DATE_FIELD = 'Transaction date or date and time'


def read_file_content(f):
    df = pd.DataFrame()
    warnings.simplefilter('ignore')
    if f.is_file() and f.name[:2] != '~$':
        try:
            df = pd.read_excel(f, header=0, engine='openpyxl')
        except Exception as e:
            print(f'error: {e} es {e.__str__}')
            logging.exception(msg=f"ERR: {e}\nazonkivul: {e.__str__()}")
    if df.shape[0] != 0:  # only if there is any content
        record_count = df.shape[0]
        currencies = df['Price currency'].unique()
        total = round(df[SUM_FIELD].sum(), 3)
        date_borders = util.get_df_dates(DATE_FIELD, 3, df)
        print(f"'{f.name}', {record_count} db record, osszeg: {total:10,.2f}, {currencies}, {date_borders}")
        return df, record_count, currencies[0], total, date_borders


def bibliotheca(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    total_df = pd.DataFrame()
    all_row_count = 0
    all_sums = 0
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        print('BIBLIOTHECA')
        for f in files:
            df_props = read_file_content(f)
            if df_props:
                current_df, rc, currency, total, dates = df_props
                total_df = pd.concat([total_df, current_df])
                all_row_count += rc
                all_sums += total
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc, currency, '', total, dates[0], dates[1]))
        # action append: replace give a row size error - before the change to other types part in get_types
        # !!! row size
        sqw.write_to_db(total_df, TABLE, field_lens='mas', action='replace', hova=hova)
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, all_sum: {all_sums}, {all_row_count} records\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    bibliotheca('0')


if __name__ == '__main__':
    main()
