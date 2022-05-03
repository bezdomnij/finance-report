from pathlib import Path
import pandas as pd
from result import Result
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
    res = []
    df = pd.DataFrame()
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        # only where source is a single file, and we think the latest is best
        files = util.get_latest_file(files, '.csv')
        for f in files:
            if f.is_file() and (FILENAME in f.stem or 'bn' in f.stem) and f.suffix.lower() == '.csv':
                df = pd.read_csv(f, header=0, sep=',')
                cols = df.columns
                print(f"{f.parents[0].stem.lower()} | {df.shape[0]} rows, {df.shape[1]}, columns")
                if len(cols) == 36:
                    df.drop(df.columns[[35]], axis=1, inplace=True)
                print(f"{f.parents[0].stem.lower()} | {df.shape[0]} rows, {df.shape[1]}, columns")
                record_count = df.shape[0]
                total = calc_sum(df)
                sqw.write_to_db(df, TABLE, action='replace', field_lens='mas', hova=hova)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total {total}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', total))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    bn('19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='w')
    main()
