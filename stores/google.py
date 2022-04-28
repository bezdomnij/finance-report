import logging
from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH, HOVA
import pandas as pd
import util
from engineer import sql_writer as sqw

DATA_DIR = 'google'
TABLE = 'stg_fin2_12_googleplay'


def google(hova=HOVA):
    df = pd.DataFrame()
    src = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(src)
    if files:
        for f in src.iterdir():
            if f.suffix == '':
                continue
            ftype, period = util.check_google_file_name(f.name)
            year, month = period
            if ftype == 'gg' and int(month) == 2:
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
        sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    google(hova='19')
