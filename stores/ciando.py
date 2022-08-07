from pathlib import Path
import pandas as pd
import warnings
from util import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_fin2_22_ciando'
FILENAME = 'Content_2_Connect_71290'
DATA_DIR = 'ciando'
SUM_FIELD = 'Total publisher'


def get_dates(fname):
    months = {
        'Q1': ['10', '11', '12', '01', '02', '03'],
        'Q2': ['01', '02', '03', '04', '05', '06'],
        'Q3': ['04', '05', '06', '07', '08', '09'],
        'Q4': ['07', '08', '09', '10', '11', '12']
    }
    quarter = ''
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    fname_parts = fname.split('-')
    for i, q in enumerate(quarters):
        quarter = quarters[i] if quarters[i] == fname_parts[0] else None
        if quarter:
            break
    dates = {}
    if quarter:
        date_pool = months[quarter]
        for d in date_pool:
            yr = int(fname_parts[1]) - 1 if quarter == 'Q1' and d in ('10', '11', '12') else int(fname_parts[1])
            dates[d] = str(yr) + '-' + d + '-' + '15'
    return dates


def ciando(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    files = util.get_file_list(p)
    print(files)
    pd.options.mode.chained_assignment = None
    # file, table, hova, sum_field, na_field, header = 0
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
                dates = get_dates(f.stem)
                print(dates)

                record_count, szumma = 0, 0
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("always")
                    df = pd.read_excel(f, header=0, index_col=None)  # , engine='openpyxl')  # ???
                try:
                    df = df[df['Data convers'].notna()]
                except KeyError as e:
                    print(f"KEY error, {e}, nothing is written.")
                try:
                    szumma = round(df[SUM_FIELD].sum(), 3)
                except KeyError as e:
                    print(f"!!!ERROR ---{f.name}--- ERROR!!! Fields changed")

                record_count = df.shape[0]
                # print(df.columns)
                print(
                    f"{f.parents[0].stem.lower()} | file: {f.stem},  {record_count} records, total: "
                    f"{round(szumma, 3):9,.2f}")
                sqw.write_to_db(df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)
                #
                # record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'Data convers', header=0)
                print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'EUR', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    ciando(hova='0')


if __name__ == '__main__':
    main()
