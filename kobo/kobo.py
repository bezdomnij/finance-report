from pathlib import Path

import util
from engineer import sql_writer as sqw

TABLE_1 = 'stg_fin2_2_kobo_drm'
TABLE_2 = 'stg_fin2_2_kobo_nodrm'
FILENAME = 'PublishDrive Kft_CONTENT2CONNECT'
SOURCE_DIR = '2022_02_february'
DATA_DIR = 'kobo'
REPORT_MONTH = '2022_02_february'
SUM_FIELD = 'Net Due (Payable Currency)'


def kobo(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    for f in p.iterdir():
        marker = '_NODRM'
        if f.is_file() and f.stem[:2] != '~$' and 'Sub' not in f.stem:
            df2 = util.get_proper_df(f)
            szumma = df2[SUM_FIELD].sum()
            size = df2.shape[0]
            print('!!! A frame merete', df2.shape[0])
            if 'DRM' in f.stem:
                marker = '_DRM'
                print(f"{DATA_DIR}{marker}, {REPORT_MONTH}, {size} records, total: {szumma:-12,.3f}")
                sqw.write_to_db(df2, TABLE_1, hova=hova, field_lens='vchall')
            else:
                print(f"{DATA_DIR}{marker}, {REPORT_MONTH}, {size} records, total: {szumma:-12,.3f}")
                sqw.write_to_db(df2, TABLE_2, hova=hova, field_lens='vchall')


def main():
    # kobo('h:/NextCloud/Finance', hova='0')
    kobo('/Users/frank/pd/Nextcloud', hova='pd')


if __name__ == '__main__':
    main()
