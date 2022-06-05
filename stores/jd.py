from pathlib import Path
import pandas as pd
from result import Result
import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
from datetime import date, MINYEAR, MAXYEAR

TABLE = 'stg_fin2_45_jd'
FILENAME = 'Order JD_PublishDrive_202204(Jan to Mar,2022)'
DATA_DIR = 'JD'
SUM_FIELD = 'Payment Amount'
DATE_FIELD = 'Sales Date'


def get_proper_df(df0):
    col2 = [col.strip() for col in df0.columns]
    renamed_cols = dict(zip(df0.columns, col2))
    df2 = df0.rename(columns=renamed_cols)
    return df2


def jd(hova='0'):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    print(files)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
                df0 = pd.read_excel(f, header=7, index_col=None)
                df = get_proper_df(df0)
                df = df.iloc[:-2]
                df.info()
                szumma = round(df[SUM_FIELD].sum(), 3)
                df['Sales Date'] = pd.to_datetime(df['Sales Date']).dt.date
                begin = df['Sales Date'].min()
                end = df['Sales Date'].max()
                record_count = df.shape[0]
                sqw.write_to_db(df, TABLE, hova=hova, field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'GBP',
                                  '', szumma, begin, end))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    jd('pd')


if __name__ == '__main__':
    main()
