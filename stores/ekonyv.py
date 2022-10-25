import re
from datetime import datetime
from pathlib import Path
import pandas as pd
from result import Result
import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_6_ekonyvhu'
# FILENAME = '-ekonyv-fogyas'
FILENAME = 'ekonyv_fogyas'
DATA_DIR = 'ekonyv'
SUM_FIELD = 'Nettó fizetendő'


def get_filename_dates(stem):
    # rp = r'\b([0-1][0-9]-publishdrive-202[0-9])-(\w+)(-ekonyv-fogyas)'
    "06-publishdrive-2022-junius-ekonyv_fogyas.xlsx"
    rp = r'\b([0-1][0-9]-publishdrive-202[0-9])-(\w+)-(ekonyv_fogyas)'
    pattern = re.compile(rp)
    r = re.match(pattern, stem)
    parts = r.group(1).split('-')
    try:
        month = int(parts[0])
        year = int(parts[2])
    except ValueError as e:
        print(f"No usable date in filename, {e}")
        return datetime(1, 1, 1), datetime(9999, 1, 1)
    else:
        last_day = util.MAX_DAYS[month]
        begin = datetime.strptime(f"{year}-{month}-01", '%Y-%m-%d').date()
        end = datetime.strptime(f"{year}-{month}-{last_day}", '%Y-%m-%d').date()
        return begin, end


def ekonyv(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files = util.get_latest_file(files, '.xlsx')
        for f in files:
            # if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$':  # and FILENAME in f.stem:
            dates = get_filename_dates(f.stem)
            # df = pd.read_excel(f, sheet_name='PublishDrive', header=12)
            df = pd.read_excel(f, header=12)
            df.rename(columns={'Cím ': 'Cím'}, inplace=True)  # NON-STANDARD: remove space from field name

            df = df[df['ISBN'].notna()]  # drop lines below data
            df['ISBN'] = df['ISBN'].astype('int64')  # otherwise, a .0 is put to the end
            record_count = df.shape[0]
            # print(f"Összesen ekönyv: {round(df['Nettó fizetendő'].sum(), 2)}")
            sqw.write_to_db(df, TABLE, hova=hova, action='replace', field_lens='vchall')
            szumma = round(df[SUM_FIELD].sum(), 0)
            print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.0f}\n")
            res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                              'HUF', '', szumma, dates[0], dates[1]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    ekonyv('19')


if __name__ == '__main__':
    main()
