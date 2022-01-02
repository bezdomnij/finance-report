import logging
from pathlib import Path

import pandas as pd

from checker import data_checker
from engineer import sql_writer as sqw


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


def make_df(files, amazon):
    srv = '19'
    # srv = 'pd'
    for f in files:
        df = pd.read_excel(f, header=0, index_col=None)
        if ' ' in df.columns:
            df.drop(df.columns[[27]], axis=1, inplace=True)
        # df.dropna(axis='columns', inplace=True, how='any')  # nem mukodik
        print(df.columns)
        too_many_chars = data_checker.d_checker(df=df, right_length=255)
        if too_many_chars:
            print(f'Look out, "{f.name}" has extra lengths: {too_many_chars}')
        sqw.write_to_db(df, amazon[f], db_name='stage', action='replace', hova=srv)


def amz_read(dirpath):
    p = Path(dirpath)
    amazon = {}
    files = [item for item in p.iterdir() if item.suffix == '.xlsx']
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
        print(f"Directory not clean, has {len(files)} items.")
        return
    make_df(files, amazon)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w')
    amz_read('/Users/frank/pd/finance_report/amazon')
