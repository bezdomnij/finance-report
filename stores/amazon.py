import logging
from pathlib import Path

import pandas as pd

from checker import data_checker
from engineer import sql_writer as sqw

SOURCE_DIR = '2022_02_february'
DATA_DIR = 'amazon'


def write_to_db(df, table_name, hova='19', extras=None):
    print('Started to connect to db...')
    if extras is None:
        extras = {}
    engine = sqw.get_engine(hova)
    types = sqw.get_types(df, extras)
    connection = engine.connect()
    try:
        df.to_sql(table_name, connection, if_exists='replace', index=False,
                  method='multi', chunksize=5000, dtype=types)
    except Exception as e:
        logging.exception(e)
        print(f'BIG RED FLAG, this is, {e.__str__}: check the logfile for details!!!{table_name}')
    else:
        print(f"Table {table_name} is written to successfully.\n")
    finally:
        connection.close()
        # engine.dispose()


def make_df(files, amazon, hova='0'):
    marker = 'KEP'
    for f in files:
        df = pd.read_excel(f, header=0, index_col=None)
        if ' ' in df.columns:
            df.drop(df.columns[[27]], axis=1, inplace=True)
        too_many_chars = data_checker.d_checker(df=df, right_length=255)
        if too_many_chars:
            print(f'Look out, "{f.name}" has extra lengths: {too_many_chars}')

        szumma = df['Payment Amount'].sum()
        print(f"\n{DATA_DIR}_{marker}, {SOURCE_DIR}, total: {szumma:-10,.3f}, \n{df.shape[0]} records")

        if 'KEP' in f.stem:
            currencies = df['Payment Amount Currency'].unique()
            currencies.sort()
            for c in currencies:
                df2 = df[df['Payment Amount Currency'] == c]
                print(f"{c}: {df2['Payment Amount'].sum():-18,.2f}")

        if 'POD' in f.stem:
            currencies = df['Royalty Amount Currency'].unique()
            marker = 'POD'
            df = df.sort_values(by=['Royalty Amount Currency'])
            currencies.sort()
            for c in currencies:
                df2 = df[df['Royalty Amount Currency'] == c]
                print(f"{c}: {df2['Payment Amount'].sum():-18,.2f}")

        sqw.write_to_db(df, amazon[f], db_name='stage', action='replace', hova=hova, field_lens='vchall')


def amz_read(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    print(p)
    amazon = {}
    files = [item for item in p.iterdir() if item.suffix == '.xlsx' and item.stem[:2] != '~$']
    if len(files) == 2:
        for item in files:
            if 'kep_print_dashboard' in item.stem or 'amazon_POD' in item.stem:
                amazon[item] = 'stg_fin2_30666_AmazonPOD'
            elif 'kep_dashboard' in item.stem or 'amazon_KEP' in item.stem:
                amazon[item] = 'stg_fin2_10666_Amazon_kep'
            else:
                print(f'Not regular amazon file in here, {dirpath}')
                return
    else:
        print(f"Directory content not clean, has {len(files)} items.")
        return
    make_df(files, amazon, hova)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='a')
    # amz_read('/Users/frank/pd/Nextcloud/szamitas', hova='0')
    amz_read('h:/Nextcloud/Finance/szamitas', hova='pd')
