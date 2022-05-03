from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from result import Result

TABLE = 'stg_fin2_15_dibook_v2'
DATA_DIR = 'dibook'
FILENAME = 'Elsz'
SUM_FIELD = 'Beszállító árbevétel összeg nettó'


def dibook(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files):
        files = util.get_latest_file(files, '.xls')
        for f in files:
            if f.is_file() and f.suffix in ['.xls', '.xlsx'] and (FILENAME in f.stem or 'DIBOOK' in f.stem):
                dimensions = util.get_content_xl_onesheet(f, TABLE, hova=hova, sum_field=SUM_FIELD,
                                                          na_field='ISBN', header=0)
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {dimensions[0]} records, total: {dimensions[1]:-16,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, dimensions[0], 'HUF', '', dimensions[1]))
    else:
        util.empty(DATA_DIR)
    return res


if __name__ == '__main__':
    dibook(hova='0')
