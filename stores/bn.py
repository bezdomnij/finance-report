from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
import logging
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_5_bn'
FILENAME = 'export'
DATA_DIR = 'bn'


def calc_sum(df):
    # print(df.info)
    return round(df['Total Cost Payment Currency'].sum(), 3)


def bn(hova=HOVA):
    """
    BN is a one-file solution
    :param hova: write to which server
    :return:
    """
    df = pd.DataFrame()
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files = util.get_latest_file(files,
                                     '.csv')  # only where source is a single file, and we think the latest is best
        for f in files:
            if f.is_file() and (FILENAME in f.stem or 'bn' in f.stem) and f.suffix.lower() == '.csv':
                df = pd.read_csv(f, header=0, sep=',')
                cols = df.columns
                print(f"{f.parents[0].stem.lower()} | {df.shape[0]} rows, {df.shape[1]}, columns")
                if len(cols) == 36:
                    df.drop(df.columns[[35]], axis=1, inplace=True)
                print(f"{f.parents[0].stem.lower()} | {df.shape[0]} rows, {df.shape[1]}, columns")

        sqw.write_to_db(df, TABLE, action='replace', field_lens='mas', hova=hova)
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {df.shape[0]} records, total {calc_sum(df)}\n")
    else:
        util.empty(DATA_DIR)


def main():
    bn('19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='w')
    main()
