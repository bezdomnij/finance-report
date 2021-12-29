import logging
from pathlib import Path

import numpy as np
import pandas as pd
import sqlalchemy.exc

from engineer import sql_writer as sqw


def write_to_db(df, table_name, hova='19', milyen="mindegy"):
    connection = None
    try:
        engine = sqw.get_engine(hova)
        connection = engine.connect()
    except sqlalchemy.exc.OperationalError as e:
        print(f'fuck, {e}')
    types = sqw.get_types(df, milyen)
    try:
        df.to_sql(table_name, connection, if_exists='replace', index=False,
                  method='multi', chunksize=5000, dtype=types)
    except ValueError as vx:
        print('ERROR!!! df not created : ', vx)
    else:
        print(f"Table {table_name} is written to successfully.")
    finally:
        try:
            connection.close()
        except AttributeError as e:
            print(f'Nothing to close, no connection. Error: {e}')


def google_audio(table='stg_fin2_20012_google_audio', hova='19'):
    files = []
    df = pd.DataFrame()
    finrep_dir = Path('h:/NextCloud/Finance/szamitas/2021_10_oktober')
    # finrep_dir = Path('/Users/frank/pd/finance_report')
    src = finrep_dir / 'google_audio'
    for f in src.iterdir():
        if f.suffix == '.csv':
            files.append(f)
    if len(files) == 1:
        try:
            df = pd.read_csv(files[0], encoding='utf-16', sep='\t', header=0, index_col=None)
        except Exception as e:
            print(f"mar konvertaltuk..., error: {e}")
            df = pd.read_csv(files[0], sep='\t', header=0, index_col=None)
        finally:
            print(df.info)
            print(df['Earnings Amount'].astype(float).sum())
            write_to_db(df, table, hova)
    else:
        print('odaszemetelt valaki, exiting...')


def google(table='stg_fin2_12_googleplay', hova='19'):
    logging.basicConfig(level=logging.ERROR, filename='datacamp.log')
    files = []
    df = pd.DataFrame()
    finrep_dir = Path('h:/NextCloud/Finance/szamitas/2021_10_oktober')
    src = finrep_dir / 'google'
    for f in src.iterdir():
        if f.suffix == '.csv':
            files.append(f)
    if len(files) == 1:
        try:
            df = pd.read_csv(files[0], encoding='utf-16', sep='\t', header=0, index_col=None)
        except Exception as e:
            print(f"mar konvertaltuk..., error: {e}")
            df = pd.read_csv(files[0], sep='\t', header=0, index_col=None)
        finally:
            print(df.columns)
            df['Earnings Amount'] = df['Earnings Amount'].str.replace(',', '.')
            print(df['Earnings Amount'].astype(float).sum())
            titt = np.asarray(df['Title'])
            for _ in titt:
                if len(_) > 255:
                    print(_, "|||", len(_))
            print(titt.shape)
            write_to_db(df, table, hova, 'mindegy')
    else:
        print('odaszemetelt valaki, exiting...')


if __name__ == '__main__':
    google_audio()
