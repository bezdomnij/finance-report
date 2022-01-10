import logging
from pathlib import Path

import pandas as pd
from util import util
from engineer import sql_writer as sqw


def google(finrep_dir, table='stg_fin2_12_googleplay', hova='19'):
    files = []
    df = pd.DataFrame()
    src = Path(finrep_dir).joinpath('google')
    for f in src.iterdir():
        if f.suffix == '':
            continue
        ftype, period = util.check_google_file_name(f.name)
        year, month = period
        if ftype == 'gg' and int(month) == 12:
            files.append(f)
            logging.info(msg=f'file found:{f}')
    for f in files:
        try:
            df = pd.read_csv(f, encoding='utf-8', sep='\t', header=0, index_col=None)
        except Exception as e:
            logging.exception(msg=f'error!!! {e}')
            # print(f"az ebooks file nem utf-16..., error: {e}")
            df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
        finally:
            # print(df.columns)
            # print(df.info)
            df['Earnings Amount'] = df['Earnings Amount'].str.replace(',', '.')
            print(f"{f.name} SUM: {df['Earnings Amount'].astype(float).sum():.2f}, row count: {df.shape[0]}")
            # print(f'{f.name} row count', df.shape[0])
    # sqw.write_to_db(df, table, action='replace', hova=hova, field_lens='mas')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    google('/Users/frank/pd/finance_report', hova='19')
# google('h:/NextCloud/Finance/szamitas/2021_11_november')
