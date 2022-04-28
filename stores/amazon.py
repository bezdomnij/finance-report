import logging
from pathlib import Path
import util
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH
from checker import data_checker
from engineer import sql_writer as sqw

DATA_DIR = 'amazon'


#
# def write_to_db(df, table_name, hova='19', extras=None):
#     print('Started to connect to db...')
#     if extras is None:
#         extras = {}
#     engine = sqw.get_engine(hova)
#     types = sqw.get_types(df, extras)
#     connection = engine.connect()
#     try:
#         df.to_sql(table_name, connection, if_exists='replace', index=False,
#                   method='multi', chunksize=5000, dtype=types)
#     except Exception as e:
#         logging.exception(e)
#         print(f'BIG RED FLAG, this is, {e.__str__}: check the logfile for details!!!{table_name}')
#     else:
#         print(f"Table {table_name} is written to successfully.\n")
#     finally:
#         connection.close()
# engine.dispose()


def make_df(files, amazon, hova='0'):
    for f in files:
        marker = 'KEP'
        df = pd.read_excel(f, header=0, index_col=None)
        if ' ' in df.columns:
            df.drop(df.columns[[27]], axis=1, inplace=True)
        too_many_chars = data_checker.d_checker(df=df, right_length=255)
        if too_many_chars:
            print(f'Look out, "{f.name}" has extra lengths: {too_many_chars}')

        szumma = df['Payment Amount'].sum()

        if 'KEP_DASH' in f.stem.upper():
            currencies = df['Payment Amount Currency'].unique()
            currencies.sort()
            for c in currencies:
                df2 = df[df['Payment Amount Currency'] == c]
                print(f"{c}: {df2['Payment Amount'].sum():-18,.2f}")

        if 'PRINT_DASH' in f.stem.upper():
            currencies = df['Royalty Amount Currency'].unique()
            marker = 'POD'
            df = df.sort_values(by=['Royalty Amount Currency'])
            currencies.sort()
            for c in currencies:
                df2 = df[df['Royalty Amount Currency'] == c]
                print(f"{c}: {df2['Payment Amount'].sum():-18,.2f}")

        print(f"\n{DATA_DIR.upper()}_{marker}, {REPORT_MONTH}, total: {szumma:-10,.2f}, \n{df.shape[0]} records")
        sqw.write_to_db(df, amazon[f], db_name='stage', action='replace', hova=hova, field_lens='vchall')


def amz_read(hova='0'):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    print(p)
    amazon = {}
    files = util.get_file_list(p)
    if files:
        files = [f for f in files if f.suffix == '.xlsx' and f.stem[:2] != '~$']
        if len(files) == 2:
            for item in files:
                if 'kep_print_dashboard' in item.stem or 'amazon_POD' in item.stem:
                    amazon[item] = 'stg_fin2_30666_AmazonPOD'
                elif 'kep_dashboard' in item.stem or 'amazon_KEP' in item.stem:
                    amazon[item] = 'stg_fin2_10666_Amazon_kep'
                else:
                    print(f'Not regular amazon file in here, {item}')
                    return
        else:
            print(f"Directory content not clean, has {len(files)} items.")
            return
        make_df(files, amazon, hova)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../datacamp.log', filemode='a')
    amz_read(hova='19')
