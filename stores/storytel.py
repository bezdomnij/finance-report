from pathlib import Path

import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE_1 = 'stg_fin2_25_overdrive'
TABLE_2 = 'stg_fin2_20025_overdrive_audio'
FILENAME = 'havi elszámolás_'
DATA_DIR = 'overdrive'
SUM_FIELD = 'Amt owed USD'


def storytel(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    record_count = 0
    if files is None:
        return
    if len(files) > 0:
        print(p)
        for f in files:
            szumma = 0
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
                df = pd.read_excel(f, header=0)
                df_audio = df.loc[df['Format'].isin(['OverDrive MP3 Audiobook', 'OverDrive Listen'])]
                szm_a = df_audio[SUM_FIELD].sum()
                rc_a = df_audio.shape[0]
                df_ebook = df.loc[df['Format'].isin(['OverDrive Read', 'Adobe EPUB eBook'])]
                szm_e = df_ebook[SUM_FIELD].sum()
                rc_e = df_ebook.shape[0]
                print(rc_a, szm_a)
                print(rc_e, szm_e)
                # print(f"{szm:-10.2f} {s}, records: {df.shape[0]}")
                # rc = df.shape[0]
                # res.append(Result(DATA_DIR.upper(), REPORT_MONTH, rc, 'USD', s, szm))
                # szumma += szm
                # record_count += rc
                # table = TABLE + s.lower()
                # sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')
                # print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total {szumma:10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    storytel(hova='0')


if __name__ == '__main__':
    main()
