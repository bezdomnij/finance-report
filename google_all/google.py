import logging
from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


def google(finrep_dir, table='stg_fin2_12_googleplay', hova='19'):
    files = []
    df = pd.DataFrame()
    # finrep_dir = Path('h:/NextCloud/Finance/szamitas/2021_10_oktober')
    # finrep_dir = Path('/Users/frank/pd/finance_report')
    src = Path(finrep_dir).joinpath('google')
    for f in src.iterdir():
        if f.suffix == '.csv':
            files.append(f)
            logging.info(msg=f'file found:{f}')
    if len(files) == 1:
        try:
            df = pd.read_csv(files[0], encoding='utf-16', sep='\t', header=0, index_col=None)
        except Exception as e:
            logging.exception(msg=f'error!!! {e}')
            print(f"mar konvertaltuk..., error: {e}")
            df = pd.read_csv(files[0], sep='\t', header=0, index_col=None)
        finally:
            print(df.columns)
            print(df.info)
            df['Earnings Amount'] = df['Earnings Amount'].str.replace(',', '.')
            print('sum: ', df['Earnings Amount'].astype(float).sum())
            print('row count', df.shape[0])
            sqw.write_to_db(df, table, action='replace', hova=hova)
    else:
        print('odaszemetelt valaki, exiting...')


if __name__ == '__main__':
    google()
