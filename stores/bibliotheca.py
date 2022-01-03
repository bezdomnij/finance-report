import logging
import warnings
from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


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
        print(f"Itt van barmi: '{f.name}', {df.shape[0]} db record")
        return df, df.shape[0]


def main(dirpath, hova='19'):
    p = Path(dirpath).joinpath('bibliotheca')
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
    print("Bibliotheca")
    print(all_row_count)
    sqw.write_to_db(total, table_name, field_lens='mas', action='replace', hova=hova)
    # action append: replace give a row size error - before the change to other types part in get_types


if __name__ == '__main__':
    directory = 'h:/NextCloud/Finance/2021_11_november'
    main(directory)
