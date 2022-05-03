import logging
from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH, HOVA
import pandas as pd
import util
from engineer import sql_writer as sqw
from result import Result

DATA_DIR = 'google'
TABLE = 'stg_fin2_12_googleplay'


def google(hova=HOVA):
    res = []
    df = pd.DataFrame()
    src = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(src)
    if files is None:
        return
    if len(files) > 0:
        for f in src.iterdir():
            if f.suffix == '':
                continue
        for f in files:
            try:
                df = pd.read_csv(f, encoding='utf-8', sep='\t', header=0, index_col=None)
            except Exception as e:
                logging.exception(msg=f'error!!! {e}')
                # print(f"az ebooks file nem utf-16..., error: {e}")
                df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
            finally:
                print(f.stem)
                df['Earnings Amount'] = df['Earnings Amount'].str.replace(',', '.')
                sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')
                record_count = df.shape[0]
                szumma = df['Earnings Amount'].astype(float).sum()
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, "
                      f"total: {szumma:.2f}, \n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    google(hova='0')
