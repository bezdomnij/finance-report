from pathlib import Path
import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, HOVA, REPORT_MONTH
from result import Result

TABLE = 'stg_fin2_20032_bookmate_audio'
FILENAME = 'PublishDrive__Content_2_Connect__Audio_'
DATA_DIR = 'bookmate_audio'
SUM_FIELD = 'Converted Revenue'


def bookmate_audio(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    files = util.get_latest_files(files, 3)
    rc_all = 0
    szum_all = 0.0
    df_all = pd.DataFrame()
    if files is None:
        return
    if len(files):
        for f in files:
            if f.is_file() and FILENAME in f.stem and f.stem[:2] != '~$':
                df, record_count, szumma = work_on_df(f)
                rc_all += record_count
                szum_all += szumma
                df_all = pd.concat([df_all, df], ignore_index=True)
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', szumma))
                print(f"{DATA_DIR.upper()}, file: {f.stem}, {record_count} records, total: {szumma:-10,.2f}")
        sqw.write_to_db(df_all, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)
        print(f"{DATA_DIR.upper()},\treport: {REPORT_MONTH}, {rc_all} records, total: {szum_all:-10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def work_on_df(f):
    df = pd.read_excel(f, header=0, index_col=None)
    new_cols = [col.strip() for col in df.columns]
    cols_map = dict(zip(df.columns, new_cols))
    df.rename(columns=cols_map, inplace=True)
    df = df.drop(df[df['Book title'] == 'Grand total:'].index)
    df['sale_date'] = REPORT_MONTH[:4] + '-' + REPORT_MONTH[5:7] + '-15'
    szumma = df[SUM_FIELD].sum()
    record_count = df.shape[0]
    return df, record_count, szumma


def main():
    bookmate_audio(hova='19')


if __name__ == '__main__':
    main()
