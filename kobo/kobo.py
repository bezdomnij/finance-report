from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH
import util
from engineer import sql_writer as sqw

TABLE_1 = 'stg_fin2_2_kobo_drm'
TABLE_2 = 'stg_fin2_2_kobo_nodrm'
FILENAME = 'PublishDrive Kft_CONTENT2CONNECT'
DATA_DIR = 'kobo'
SUM_FIELD = 'Net Due (Payable Currency)'


def kobo(hova='0'):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)

    if files is None:
        return
    if len(files) > 0:
        for f in p.iterdir():
            marker = '_NODRM'
            if f.is_file() and f.stem[:2] != '~$' and 'Sub' not in f.stem:
                df2 = util.get_proper_df(f)
                szumma = df2[SUM_FIELD].sum()
                size = df2.shape[0]
                print('!!! A frame merete', df2.shape[0])
                if 'DRM' in f.stem:
                    marker = '_DRM'
                    print(f)
                    print(f"{DATA_DIR}{marker}, {REPORT_MONTH}, {size} records, total: {szumma:-12,.3f}")
                    sqw.write_to_db(df2, TABLE_1, hova=hova, field_lens='vchall')
                else:
                    print(f)
                    print(f"{DATA_DIR}{marker}, {REPORT_MONTH}, {size} records, total: {szumma:-12,.3f}")
                    sqw.write_to_db(df2, TABLE_2, hova=hova, field_lens='vchall')
    else:
        print(f"Looks like the {DATA_DIR} directory is empty.")


def main():
    kobo(hova='0')


if __name__ == '__main__':
    main()
