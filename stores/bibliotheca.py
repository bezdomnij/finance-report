import logging
import warnings
from pathlib import Path

import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH
from engineer import sql_writer as sqw

DATA_DIR = 'bibliotheca'
TABLE = 'stg_fin2_39_bibliotheca'


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
        print(f"{f.parents[0].stem.lower()} barmi is, itt: '{f.name}', {df.shape[0]} db record", end=" -- ")
        print(round(df['Total proceeds due to publisher'].sum(), 2))
        return df, df.shape[0]


def bibliotheca(hova='0'):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    total_df = pd.DataFrame()
    all_row_count = 0
    files = util.get_file_list(p)
    files = [f for f in files if f.suffix == '.xlsx']
    # multiple files system!!!
    if files:
        for f in files:
            whatever = read_file_content(f)
            if whatever:
                current_df, rc = whatever
                total_df = pd.concat([total_df, current_df])
                all_row_count += rc
        print(f"{DATA_DIR.upper()} {all_row_count}, db record")
        # action append: replace give a row size error - before the change to other types part in get_types
        # !!! row size
        sqw.write_to_db(total_df, TABLE, field_lens='mas', action='replace', hova=hova)


def main():
    bibliotheca('0')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='w')
    main()
