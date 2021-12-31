from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


def google_audio(table='stg_fin2_20012_google_audio', hova='19'):
    files = []
    df = pd.DataFrame()
    # finrep_dir = Path('h:/NextCloud/Finance/szamitas/2021_11_november')
    finrep_dir = Path('/Users/frank/pd/finance_report')
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
            print(df.columns)
            print(df.info)
            print(df['Earnings Amount'].astype(float).sum())
            sqw.write_to_db(df, table, action='replace', hova=hova)
    else:
        print('odaszemetelt valaki, check dir contents...')


if __name__ == '__main__':
    google_audio()
