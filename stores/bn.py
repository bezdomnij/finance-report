from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


def calc_sum(df):
    print(df.info)
    return df['Total Cost Payment Currency'].sum()


def main(dirpath, hova='19'):
    p = Path(dirpath) / 'bn'
    file = p / 'bn.csv'
    df = pd.read_csv(file, header=0, sep=',')

    print(df.shape[0], df.shape[1])
    df.drop(df.columns[[35]], axis=1, inplace=True)
    print(df.shape[0], df.shape[1])

    print(calc_sum(df))
    sqw.write_to_db(df, 'stg_fin2_5_bn', hova=hova)


if __name__ == '__main__':
    main('/Users/frank/pd/finance_report', '19')
