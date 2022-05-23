"""
NONSTANDARD location - jan-march in one run
-- report arrives on time or not
turns out the details' version is the winner: Date van, units sold nincs, mert 1 az sp-ben is
this is how the sp was set up anyway, quantity 1
"""
from datetime import datetime
from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH
import util
import re

TABLE = 'stg_fin2_21_esentral'
# FILENAME = '_MYR'
# FILENAME = 'item'
SOURCE_DIR = REPORT_MONTH  # itt a source_dir NEM a report_month, hanem +1
# SOURCE_DIR = '2022_04_april'
DATA_DIR = 'esentral'  # Path is different
SUM_FIELD = 'Earning'


def make_date(year_month):
    try:
        int(year_month)
    except Exception as e:
        print(f'FAILURE to convert to date, {e}')
        return
    base = str(year_month)
    yr = base[:4]
    mnth = base[4:]
    str_datum = yr + '-' + mnth + '-15'
    return datetime.strptime(str_datum, '%Y-%m-%d').date()


def get_date_currency(filename):
    """
    assumes filename has yearmonth in it plus the currency
    according to pattern
    :param filename: string with - hopefully - 3 parts yearmonth, currency, report type
    :return:
    """
    parts = filename.split('_')
    datum = make_date(parts[0])
    return datum, parts[1]


def esentral(hova='0'):
    """
    "Date","ISBN","Imprint","Title","Sale Price","Earning"
    "ISBN","Imprint","Title","Price","Unit","Total Sale","Earning"
    types = {'isbn': sqlalchemy.types.VARCHAR(length=255),
                 'parent_isbn': sqlalchemy.types.VARCHAR(length=255),
                 'isbn_13': sqlalchemy.types.VARCHAR(length=255),
                 'compensation_type': sqlalchemy.types.VARCHAR(length=50),
                 'currency': sqlalchemy.types.VARCHAR(length=10),
                 'sale_date': sqlalchemy.types.VARCHAR(length=15),
                 'cancelled_date': sqlalchemy.types.VARCHAR(length=50)}
    """
    p = Path(MAIN_DIR).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # p = Path(MAIN_DIR).joinpath(DATA_DIR)
    df_all = pd.DataFrame()
    szumma = 0.00
    record_count = 0
    # disable chained assignments
    pd.options.mode.chained_assignment = None

    # pattern = re.compile(r"202\d(0[1-9]|1[0-2])_(MYR|IDR|SGD)_(cover|details)")  # not used, experimental
    # cover = re.compile(r"202\d(0[1-9]|1[0-2])_(MYR|IDR|SGD)_cover")  # not used, experimental
    details = re.compile(r"202\d(0[1-9]|1[0-2])_(MYR|IDR|SGD)_details")

    files = util.get_file_list(p)

    if files is None:
        return
    if len(files) > 0:
        # df_all_1 = use_merge(files, pattern)
        # df_all_2 = use_cover(cover, df_all, files, record_count, szumma)
        restricted_file_list = [f for f in files if details.match(f.stem)]
        for f in restricted_file_list:
            df = pd.read_csv(f, header=0, encoding='utf-8')
            print(f.stem)
            datum_nem, currency = get_date_currency(f.stem)
            # df['Date'] = datum
            df['Currency'] = currency
            df['Country'] = 'MY'
            szm = df[SUM_FIELD].sum()
            rc = df.shape[0]
            print(f"{f.stem}-ben {rc} records in total of {szm}")
            record_count += rc
            szumma += szm
            df_all = df_all.append(df, ignore_index=True)

        if not df_all.empty:
            # print(df_all)
            print(f"check count szamolt: {df_all.shape[0]} vs. gyujtott: {record_count}")
            print(f"check sum, szamolt: {df_all[SUM_FIELD].astype('float64').sum()} vs. gyujtott: {szumma}")
            print(f"{DATA_DIR.upper()}\treport: {REPORT_MONTH}, total: {szumma:-10,.2f}\t, {record_count} records")
            sqw.write_to_db(df_all, TABLE, hova=hova, db_name='stage', action='replace', field_lens='vchall')


def use_cover(cover, df_all, files, record_count, szumma):
    """
    using the files that are summaries of monthly transactions (units counted, no date)
    :param cover:
    :param df_all:
    :param files:
    :param record_count:
    :param szumma:
    :return:
    """
    alternative_files = [f for f in files if cover.match(f.stem)]
    for f in alternative_files:
        df = pd.read_csv(f, header=0, encoding='utf-8')
        print(f.stem)
        datum, currency = get_date_currency(f.stem)
        df['Date'] = datum
        df['Currency'] = currency
        szm = df[SUM_FIELD].sum()
        rc = df.shape[0]
        print(f"{f.stem}-ben {rc} records in total of {szm}")
        record_count += rc
        szumma += szm
        df_all = df_all.append(df)
    return df_all


def use_merge(files, pattern):  # not used in live, just an experiment
    """
    merging two types of report files to have all columns
    if the unit count is > 1 (in the incoming data) then this is not usable
    e.g. 2 items at two different times sold: 2 lines in details, 1 line in cover, results in 3 lines
    :param files: cover and details files in the directory
    :param pattern:
    :return:
    """
    df_all = pd.DataFrame()
    keys = set()
    covers, details = {}, {}
    for f in files:
        if f.is_file() and f.suffix == '.csv' and pattern.match(f.stem):
            keys.add(f.stem[:11])
            df = pd.read_csv(f, header=0, encoding='utf-8')
            if 'cover' in f.stem:
                print(f.stem)
                covers[f.stem[:-5]] = df
            elif 'details' in f.stem:
                print(f.stem)
                details[f.stem[:-7]] = df
    keys = list(keys)
    print(keys)
    for k in keys:
        df_c = covers[k]
        df_d = details[k]
        merged = pd.merge(df_d, df_c, how='outer')
        merged.info()
        szm = merged[SUM_FIELD].sum()
        print(f"{k} | record count {merged.shape[0]} records, total: {szm}")

        #     df[SUM_FIELD] = df[SUM_FIELD].str.strip().str.slice(start=1)
        #     print(f"{f.parents[0].stem.lower()} | amount {df[SUM_FIELD].astype('float64').sum()}\n")
        df_all = df_all.append(merged)
    return df_all


def main():
    # perlego('/Users/frank/pd/Nextcloud', hova='0')
    esentral(hova='19')


if __name__ == '__main__':
    main()
