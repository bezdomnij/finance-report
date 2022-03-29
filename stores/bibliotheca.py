import logging
import warnings
from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

DATA_DIR = 'bibliotheca'
SOURCE_DIR = '2022_02_february'
TABLE = 'stg_fin2_39_bibliotheca'


def read_file_content(f):
    df = pd.DataFrame()
    warnings.simplefilter('ignore')
    if f.is_file() and f.suffix == '.xlsx' and f.name[:2] != '~$':
        try:
            df = pd.read_excel(f, header=0, engine='openpyxl')
        except Exception as e:
            print(f'error: {e} es {e.__str__}')
            logging.exception(msg=f"ERR: {e}\nazonkivul: {e.__str__()}")
    if df.shape[0] != 0:  # only if there is any content
        print(f"Itt van barmi: '{f.name}', {df.shape[0]} db record", end=" -- ")
        print(round(df['Total proceeds due to publisher'].sum(), 2))
        return df, df.shape[0]


def bibliotheca(dirpath, hova='19'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    total_df = pd.DataFrame()
    all_row_count = 0

    # multiple files system!!!
    for f in p.iterdir():
        whatever = read_file_content(f)
        if whatever:
            current_df, rc = whatever
            total_df = pd.concat([total_df, current_df])
            all_row_count += rc
    print("Bibliotheca", end='  --  ')
    print(all_row_count, 'db record')
    # action append: replace give a row size error - before the change to other types part in get_types
    # !!! row size
    sqw.write_to_db(total_df, TABLE, field_lens='mas', action='replace', hova=hova)


def main():
    directory = 'h:/NextCloud/Finance/szamitas'
    # directory = '/Users/frank/pd/Nextcloud/szamitas'
    bibliotheca(directory, '19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='w')
    main()
