import logging
import warnings
from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

DATA_DIR = 'bibliotheca'
SOURCE_DIR = '2022_02_february'


def read_file_content(f):
    df = pd.DataFrame()
    warnings.simplefilter('ignore')
    if f.is_file() and f.suffix == '.xlsx' and f.name[:2] != '~$':
        try:
            df = pd.read_excel(f, header=0, engine='openpyxl')
        except Exception as e:
            print(f'error: {e} es {e.__str__}')
            logging.exception(msg=f"ERR: {e}\nazonkivul: {e.__str__()}")
    if df.shape[0] != 0:
        print(f"Itt van barmi: '{f.name}', {df.shape[0]} db record", end=" -- ")
        print(round(df['Total proceeds due to publisher'].sum(), 2))
        return df, df.shape[0]


def main(dirpath, hova='19'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    total = pd.DataFrame()
    all_row_count = 0
    table_name = 'stg_fin2_39_bibliotheca'

    # multiple files system!!!
    for f in p.iterdir():
        whatever = read_file_content(f)
        if whatever:
            current_df, rc = whatever
            total = pd.concat([total, current_df])
            all_row_count += rc
    print("Bibliotheca", end='  --  ')
    print(all_row_count, 'db record')
    sqw.write_to_db(total, table_name, field_lens='mas', action='replace', hova=hova)
    # action append: replace give a row size error - before the change to other types part in get_types


if __name__ == '__main__':
    # directory = 'h:/NextCloud/Finance/2022_01_january'
    directory = '/Users/frank/pd/Nextcloud'
    main(directory, '0')
