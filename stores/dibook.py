from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util

TABLE = 'stg_fin2_15_dibook_v2'
DATA_DIR = 'dibook'
FILENAME = 'Elsz'
SUM_FIELD = 'Beszállító árbevétel összeg nettó'


def dibook(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files):
        for f in files:
            if f.is_file() and f.suffix in ['.xls', '.xlsx'] and FILENAME in f.stem:
                dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                          na_field='ISBN', header=0)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-16,.2f}\n")
    else:
        util.empty(DATA_DIR)


if __name__ == '__main__':
    dibook(hova='19')
