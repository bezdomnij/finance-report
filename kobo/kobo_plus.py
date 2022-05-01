from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_rts2_40_koboplus'
FILENAME = 'Sub_PublishDrive Kft_CONTENT2CONNECT_DRM_'
DATA_DIR = 'kobo'
SUM_FIELD = 'Total publisher revenue share in payable currency ($)'


# adjust MONTH to pick the source file
# adjust MONTH to pick the source file


def kobo_plus(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.stem[:2] != '~$' and FILENAME in f.stem:
                df = pd.read_excel(f, sheet_name='Details', header=0, index_col=None)
                col2 = [col.strip() for col in df.columns]
                renamed_cols = dict(zip(df.columns, col2))
                df2 = df.rename(columns=renamed_cols)
                szumma = df2[SUM_FIELD].sum()
                record_count = df.shape[0]
                print(f.stem)
                sqw.write_to_db(df2, TABLE, hova=hova, field_lens='vchall')
                print(
                    f"{(DATA_DIR + ' PLUS').upper()} | {REPORT_MONTH}, {record_count:10,d} records, "
                    f"total: {szumma:10,.2f}\n")
    else:
        util.empty(DATA_DIR)


def main():
    kobo_plus(hova='0')


if __name__ == '__main__':
    main()
