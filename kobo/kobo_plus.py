from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

TABLE = 'stg_rts2_40_koboplus'
FILENAME = 'Sub_PublishDrive Kft_CONTENT2CONNECT_DRM_Feb 2022'
SOURCE_DIR = '2022_02_february'
DATA_DIR = 'kobo'
REPORT_MONTH = '2022_02_february'
SUM_FIELD = 'Total publisher revenue share in payable currency ($)'


# adjust MONTH to pick the source file
# adjust MONTH to pick the source file


def kobo_plus(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    for f in p.iterdir():
        if f.is_file() and f.stem[:2] != '~$' and FILENAME in f.stem:
            df = pd.read_excel(f, sheet_name='Details', header=0, index_col=None)
            col2 = [col.strip() for col in df.columns]
            renamed_cols = dict(zip(df.columns, col2))
            df2 = df.rename(columns=renamed_cols)
            szumma = df2[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}")
            print(df2.shape[0], 'records')
            sqw.write_to_db(df2, TABLE, hova=hova, field_lens='vchall')


def main():
    # read_kobo_plus('h:/NextCloud/Operative/Admin dev/live_sales_v2', hova='0')
    kobo_plus('/Users/frank/pd/Nextcloud', hova='pd')


if __name__ == '__main__':
    main()
