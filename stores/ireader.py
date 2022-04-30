from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_46_ireader'
FILENAME = 'PublishDrive_Monthly Sales Detail Data@'
DATA_DIR = 'ireader'
SUM_FIELD = 'Sharing Amount'


def ireader(hova=HOVA):
    """
    ireader sales needs catalog info, sales file has no isbn, just ireader id
    get the isbn from the catalog that has both
    checks structure and sums. Needs extra steps on the sql side to get isbns, some of them missing
    :param hova: sever where to write
    :return: nothing
    """
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    if len(files) > 0:
        print(p)
        for f in files:
            if f.suffix == '.csv' and FILENAME in f.stem:  # .csv!!!
                df = pd.read_csv(f, encoding='utf-8', header=0)
                print(f.name)
                record_count = df.shape[0]
                szumma = df[SUM_FIELD].sum()
                sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, total: {szumma:-10,.3f}\t{record_count:10,d} records\n")
    else:
        print(f"Looks like the `{DATA_DIR}` directory is empty.")


def main():
    ireader(hova='19')


if __name__ == '__main__':
    main()
