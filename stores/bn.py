from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

SOURCE_DIR = '2022_02_february'
DATA_DIR = 'bn'
FILENAME = 'export ('


def calc_sum(df):
    # print(df.info)
    return df['Total Cost Payment Currency'].sum()


def apple(dirpath, hova='0'):
    df = pd.DataFrame()
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)

    for f in p.iterdir():
        if f.is_file() and f.suffix == '.csv' and FILENAME in f.stem:
            df = pd.read_csv(f, header=0, sep=',')
            print(df.shape[0], df.shape[1], ' columns')
            df.drop(df.columns[[35]], axis=1, inplace=True)
            print(df.shape[0], df.shape[1], ' columns')

    print(f"BN: {df.shape[0]} db, total {calc_sum(df)}")
    sqw.write_to_db(df, 'stg_fin2_5_bn', action='replace', field_lens='mas', hova=hova)


def main():
    apple('/Users/frank/pd/Nextcloud', 'pd')


if __name__ == '__main__':
    main()
