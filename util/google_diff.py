from pathlib import Path
import os
import platform
from datetime import datetime
from engineer import sql_writer as sqw
# from stores.google_audio import get_df
import pandas as pd


def get_df(f):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
    except Exception as e:
        print(f"mar konvertaltuk..., error: {e}")
        df = pd.read_csv(f, sep='\t', header=0, index_col=None)
    finally:
        return df


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def measure_googles(dirpath, hova='0'):
    p = Path(dirpath)
    for i, f in enumerate(p.iterdir()):
        name_parts = f.stem.split('-')
        fsize = os.stat(f)
        table_name = f'size_{fsize.st_size}_{i}'
        df = get_df(f)
        df['Earnings Amount'] = df['Earnings Amount'].str.replace(',', '.')
        df_sum = str(round(df['Earnings Amount'].astype(float).sum(), 2)).replace('.', 'd')
        df_count = str(df.shape[0])
        # table_name = f'{table_name}_sum{df_sum}_rcount{df_count}_{name_parts[-1]}'
        print(table_name)
        sqw.write_to_db(df, table_name=table_name, hova=hova, field_lens='mas')


def main():
    measure_googles('/Users/frank/pd/finance_report/google_anomaly', '19')


if __name__ == '__main__':
    main()
