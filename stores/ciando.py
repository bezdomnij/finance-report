from pathlib import Path
import pandas as pd
import warnings
from collections import OrderedDict
from util import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_fin2_22_ciando'
FILENAME = 'Content_2_Connect_71290'
DATA_DIR = 'ciando'
SUM_FIELD = 'Total publisher'
KEYS = ['Title', 'eISBN_13',
        # 'ciando_04 as `ertek`', '2021-04-15 as datum',
        'Sales total', 'pub_sale_percent_ciando', 'pub_sale_percent_rp', 'pub_sale_percent_library',
        'Books', 'VAT rate', 'eladasi_egysegar', 'Total publisher']


def get_dates(fname):
    """
    filename must start with Q[1-4]-YYYY...
    :param fname:
    :return: a dict, key is month, value is the 15th of that month, ISO format
    """
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
    dates = OrderedDict()
    if quarter:
        months_pool = months[quarter]
        for m in months_pool:
            # goes back to previous year in Q1
            yr = int(fname_parts[1]) - 1 if quarter == 'Q1' and m in ('10', '11', '12') else int(fname_parts[1])
            dates[m] = str(yr) + '-' + m + '-' + '15'
    return dates


def get_part_df(df, key, dates):
    """
    create a df for each column (colum contains sale type and month information)
    :param df: full reformed df
    :param key: column of data
    :param dates: dates dict created based on column labels (type and month included in there)
    :return: a df to be added to the collection
    """
    col_keys = str(key).split('_')  # a column name contains type and month info separated by '_'
    dates_lst = list(dates.values())  # used for the Libraries column only - middle date in quarter
    # col_key is from the column name
    the_date = dates[col_keys[1]] if col_keys[0] != 'Libraries' else dates_lst[-2]

    print(KEYS)
    new_columns = KEYS.copy()
    new_columns.extend([key])
    result_df = df[new_columns]
    result_df = result_df.drop(result_df[result_df[key] == 0].index)
    result_df['datum'] = the_date
    result_df['darab'] = round(result_df[key] / result_df['eladasi_egysegar'])

    if 'ciando' in str(key):
        result_df['Total'] = result_df['eladasi_egysegar'] * result_df['darab'] * 0.7
        result_df['netto_egysegar'] = result_df['eladasi_egysegar'] * 0.7
    else:
        result_df['Total'] = result_df['eladasi_egysegar'] * result_df['darab'] * 0.6
        result_df['netto_egysegar'] = result_df['eladasi_egysegar'] * 0.6
    return result_df


def get_key_elements(columns):
    """
    those columns from all that have the sale info for sale type
    :param columns: all columns in df
    :return: a list of key columns where sale data is contained and needs to be broken up
    """
    key_els = []
    for col in columns:
        if col.split('_')[0] in ['ciando', 'rp', 'Libraries']:
            key_els.append(col)
    return key_els


def ciando(hova=HOVA):
    """
    breaks up the structure of the report to make it usable for db - each type & each book into a separate line
    uses an already modified Excel file; filename must start with Q[1-4]
    gets a date based on column header
    writes to db, to ciando alternative table. Sp is modified to take this input
    :param hova:
    :return: result object to record in log
    """
    res = []
    reformed_df = pd.DataFrame()
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)

    # disable chained assignments
    files = util.get_file_list(p)
    print(files)
    pd.options.mode.chained_assignment = None

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
                    df_orig = pd.read_excel(f, header=0, index_col=None)  # , engine='openpyxl')  # ???
                try:
                    df_orig = df_orig[df_orig['Data convers'].notna()]
                except KeyError as e:
                    print(f"KEY error, {e}, nothing is written.")
                print(df_orig.columns)
                try:
                    szumma = round(df_orig[SUM_FIELD].sum(), 3)
                except KeyError as e:
                    print(f"!!!ERROR ---{f.name}--- ERROR!!! Fields changed")
                key_elements = get_key_elements(df_orig.columns)
                for key in key_elements:
                    print(key)
                    part_df = get_part_df(df_orig, key, dates)
                    reformed_df = pd.concat([reformed_df, part_df], axis=0, ignore_index=True)
                record_count = df_orig.shape[0]
                print(reformed_df['darab'].sum())  # dropped lines with 0 amounts, may not agree with reports' sum
                print(f"{f.parents[0].stem.lower()} | file: {f.stem},  {record_count} records, total: "
                      f"{round(szumma, 3):9,.2f}")
                sqw.write_to_db(reformed_df, 'stg_fin2_22_ciando_alternative', db_name='stage', action='replace',
                                field_lens='vchall', hova=hova)
                # old way below
                # record_count, szumma = util.get_content_xl_onesheet(f, TABLE, hova, SUM_FIELD, 'Data convers', header=0)
                print(f"{DATA_DIR.upper()}, {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'EUR', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    ciando(hova='pd')


if __name__ == '__main__':
    main()
