import logging
import warnings
from pathlib import Path

import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATA_DIR = 'bibliotheca'
TABLE = 'stg_fin2_39_bibliotheca'
SUM_FIELD = 'Total proceeds due to publisher'


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
        print(f"{f.parents[0].stem.lower()} itt: '{f.name}', "
              f"{df.shape[0]} db record, osszeg: {round(df[SUM_FIELD].sum(), 2):10,.2f}")
        return df, df.shape[0]


def bibliotheca(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    total_df = pd.DataFrame()
    all_row_count = 0
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        print()
        for f in files:
            df_props = read_file_content(f)
            if df_props:
                current_df, rc = df_props
                total_df = pd.concat([total_df, current_df])
                all_row_count += rc
        # action append: replace give a row size error - before the change to other types part in get_types
        # !!! row size
        sqw.write_to_db(total_df, TABLE, field_lens='mas', action='replace', hova=hova)
        print(f"{DATA_DIR.upper()} | {all_row_count} records\n")
    else:
        util.empty(DATA_DIR)


def main():
    bibliotheca('19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='w')
    main()
