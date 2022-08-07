from pathlib import Path

import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE_1 = 'stg_fin2_25_overdrive'
TABLE_2 = 'stg_fin2_20025_overdrive_audio'
FILENAME = 'havi elsz'
DATA_DIR = 'overdrive'
SUM_FIELD = 'Amt owed USD'
DATE_FIELD = 'Date'


def overdrive(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        print(p)
        for f in files:
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
                df = pd.read_excel(f, header=0)
                df_audio = df.loc[df['Format'].isin(['OverDrive MP3 Audiobook', 'OverDrive Listen'])]
                rc_a, szm_a = get_params(df_audio)
                print(f"{DATA_DIR.upper() + '_AUDIO'} | {REPORT_MONTH}, {rc_a} records, total {szm_a:10,.2f}\n")
                sqw.write_to_db(df_audio, TABLE_2, hova=hova, action='replace', field_lens='vchall')
                date_borders = util.get_df_dates(DATE_FIELD, 1, df_audio)
                res.append(Result(DATA_DIR.upper() + '_AUDIO', REPORT_MONTH, rc_a,
                                  'USD', '', szm_a, date_borders[0], date_borders[1]))
                print(date_borders)

                df_ebook = df.loc[df['Format'].isin(['OverDrive Read', 'Adobe EPUB eBook'])]
                rc_e, szm_e = get_params(df_ebook)
                date_borders = util.get_df_dates(DATE_FIELD, 1, df_ebook)
                print(date_borders)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {rc_e} records, total {szm_e:10,.2f}\n")
                sqw.write_to_db(df_ebook, TABLE_1, hova=hova, action='replace', field_lens='vchall')
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc_e,
                                  'USD', '', szm_e, date_borders[0], date_borders[1]))

                record_count, szumma = get_params(df)
                print(f"{DATA_DIR.upper() + '_ALL'} | {REPORT_MONTH}, {record_count} records, total {szumma:10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def get_params(df):
    szm = round(df[SUM_FIELD].sum(), 3)
    rc = df.shape[0]
    # print(rc, szm)
    return rc, szm


def main():
    overdrive(hova='pd')


if __name__ == '__main__':
    main()
