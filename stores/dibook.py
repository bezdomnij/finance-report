from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH
import util

TABLE = 'stg_fin2_15_dibook_v2'
DATA_DIR = 'dibook'
FILENAME = 'Elsz'
SUM_FIELD = 'Beszállító árbevétel összeg nettó'


def dibook(hova='0'):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    for f in p.iterdir():
        if f.is_file() and f.suffix in ['.xls', '.xlsx'] and FILENAME in f.stem:
            dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                      na_field='ISBN', header=0)
            print(f"{DATA_DIR} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-10,.2f}\n")


if __name__ == '__main__':
    dibook(hova='pd')
