from pathlib import Path
import pandas as pd
from writer import sql_writer as sqw


def write_to_db(df, table_name, hova='19'):
    engine = sqw.get_engine(hova)
    connection = engine.connect()
    types = sqw.get_types(df)
    try:
        df.to_sql(table_name, connection, if_exists='replace', index=False,
                  method='multi', chunksize=20000, dtype=types)
    except ValueError as vx:
        print('ERROR!!! df not created : ', vx)
    else:
        print(f"Table {table_name} is written to successfully.")
    finally:
        connection.close()


def google_audio(table='stg_fin2_20012_google_audio', hova='19'):
    print(Path.cwd())
    files = []
    finrep_dir = Path(__file__).parents[2]
    src = finrep_dir / 'google_audio'
    for f in src.iterdir():
        if f.suffix == '.csv':
            files.append(f)
    if len(files) == 1:
        df = pd.read_csv(files[0], encoding='utf-16', sep='\t', header=0, index_col=None)
        print(df.info)
        print(df['Earnings Amount'].astype(float).sum())

        write_to_db(df, table, hova)
    else:
        print('odaszemetelt valaki, exiting...')


if __name__ == '__main__':
    google_audio()
