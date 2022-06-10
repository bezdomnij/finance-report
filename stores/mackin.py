import datetime
import re
from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE = 'stg_fin2_36_mackin_data'
FILENAME = 'PUBLISHDRIVE_EBOOKS_2022_'
DATA_DIR = 'mackin'
SUM_FIELD = 'Ext Cost'


def get_filename_dates(stem, raw, hova):
    pattern = re.compile(raw)
    m = re.match(pattern, stem)
    # print(m.group(2))
    begin = str(m.group(2)).replace('_', '-')
    # print(m.group(4))
    end = str(m.group(4)).replace('_', '-')
    print(begin, end)
    # dict_to_sql = {'date_from': [begin], 'date_to': [end]}
    dates_to_df = {'date_from': begin, 'date_to': end}
    print(dates_to_df)
    # date_df = pd.DataFrame.from_dict([dates_to_df])  # muxik, de alahuzza
    # date_df = pd.DataFrame.from_dict(dates_to_df, orient='index', columns=['date_from', 'date_to'])  # nope
    date_df = pd.DataFrame()
    date_df = date_df.append(dates_to_df, ignore_index=True)
    sqw.write_to_db(date_df, 'stg_fin2_36_mackin_date', field_lens='vchall', hova=hova)
    begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    return begin_date, end_date


def mackin(hova=HOVA):
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
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.suffix in ['.xlsx', '.xls', '.XLS'] and FILENAME in f.stem:
                raw = \
                    r'(PUBLISHDRIVE_EBOOKS_)(202[0-9]_([0][0-9]|[1][0-2])_[0-3][0-9])' \
                    r'_to_(202[0-9]_([0][0-9]|[1][0-2])_[0-3][0-9])'
                dates = get_filename_dates(f.stem, raw, hova)
                df = pd.read_excel(f, header=4)
                # print(df.columns)
                df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1)
                # print(df.shape[0])
                df = df[df['ISBN'].notna()]
                df = df[df['Title'] != 'Title']
                record_count = df.shape[0]
                szumma = df[SUM_FIELD].sum()
                sqw.write_to_db(df, TABLE, hova=hova, action='replace', field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                  'USD', '', szumma, dates[0], dates[1]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    mackin('19')


if __name__ == '__main__':
    main()
