from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from util import util
import logging
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

DATA_DIR = 'google_audio'
TABLE = 'stg_fin2_20012_google_audio'
DATE_FIELD = 'Transaction Date'


def get_df(f):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
    except Exception as e:
        print(f"mar konvertaltuk..., error: {e}")
        df = pd.read_csv(f, encoding='utf-8', sep='\t', header=0, index_col=None)
    finally:
        return df


def google_audio(hova=HOVA):
    res = []
    src = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(src)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            df = get_df(f)
            if df.shape[0] > 0:
                logging.debug(f"message is shape: {df.shape[0]}")
                sqw.write_to_db(df, TABLE, action='replace', hova=hova)
                record_count = df.shape[0]
                szumma = df['Earnings Amount'].astype(float).sum()
                date_borders = util.get_df_dates(DATE_FIELD, 3, df)
                print(
                    f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: "
                    f"{szumma:.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '',
                                  szumma, date_borders[0], date_borders[1]))
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    google_audio(hova='0')
