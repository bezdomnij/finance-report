import datetime
from pathlib import Path
import pandas as pd
from result import Result
import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
from datetime import date, MINYEAR, MAXYEAR

TABLE = 'stg_fin2_46_ireader'
FILENAME = 'PublishDrive_Monthly Sales Detail Data@'
DATA_DIR = 'ireader'
SUM_FIELD = 'Sharing Amount'
DATE_FIELD = 'Date'


def make_dates(date_field_content):
    print('EEEZ', date_field_content)
    ym = date_field_content.tolist()
    if len(ym) == 1:
        year_month = ym[0].split('-')
        try:
            year = int(year_month[0])
            month = int(year_month[1])
        except Exception as e:
            print(f"failed conversion: {e}")
            return MINYEAR, MAXYEAR
        else:
            last_day = util.MAX_DAYS[month]
            return date(year, month, 1), date(year, month, last_day)


def ireader(hova=HOVA):
    """
    ireader sales needs catalog info, sales file has no isbn, just ireader id
    get the isbn from the catalog that has both
    checks structure and sums. Needs extra steps on the sql side to get isbns, some of them missing
    :param hova: sever where to write
    :return: nothing
    """
    res = []
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
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.3f}\n")
                # df['Date'] = df['Date'] + '-15'
                # df['month'] = df['Date'].dt.month
                # df['month'] = pd.DatetimeIndex(df['Date']).month
                # report_month = df['month'].unique()
                min_date, max_date = make_dates(df['Date'].unique())
                res.append((Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                   'USD', '', szumma, min_date, max_date)))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    ireader(hova='19')


if __name__ == '__main__':
    main()
