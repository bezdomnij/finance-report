from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH

TABLE = 'stg_rts2_40_koboplus'
FILENAME = 'Sub_PublishDrive Kft_CONTENT2CONNECT_DRM_'
DATA_DIR = 'kobo'
SUM_FIELD = 'Total publisher revenue share in payable currency ($)'


# adjust MONTH to pick the source file
# adjust MONTH to pick the source file


def kobo_plus(hova='0'):
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
                print(f.stem)
                print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}")
                print(df2.shape[0], 'records')
                sqw.write_to_db(df2, TABLE, hova=hova, field_lens='vchall')
    else:
        print(f"Looks like the `{DATA_DIR}` directory is empty.")


def main():
    kobo_plus(hova='0')


if __name__ == '__main__':
    main()
