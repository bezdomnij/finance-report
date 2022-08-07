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
        date_pool = months[quarter]
        for d in date_pool:
            yr = int(fname_parts[1]) - 1 if quarter == 'Q1' and d in ('10', '11', '12') else int(fname_parts[1])
            dates[d] = str(yr) + '-' + d + '-' + '15'
    return dates


def get_part_df(df, key, dates):
    col_keys = str(key).split('_')
    dates_lst = list(dates.values())
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
    key_els = []
    for col in columns:
        if col.split('_')[0] in ['ciando', 'rp', 'Libraries']:
            key_els.append(col)
    return key_els


def ciando(hova=HOVA):
    res = []
    reformed_df = pd.DataFrame()
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
                # key_elements = ['ciando_04', 'ciando_05', 'ciando_06', 'rp_01', 'rp_02', 'rp_03', 'Libraries_02']
                key_elements = get_key_elements(df_orig.columns)
                for key in key_elements:
                    print(key)
                    part_df = get_part_df(df_orig, key, dates)
                    reformed_df = pd.concat([reformed_df, part_df], axis=0, ignore_index=True)
                record_count = df_orig.shape[0]
                print(reformed_df['darab'].sum())
                print(
                    f"{f.parents[0].stem.lower()} | file: {f.stem},  {record_count} records, total: "
                    f"{round(szumma, 3):9,.2f}")
                sqw.write_to_db(reformed_df, 'stg_fin2_22_ciando_alternative', db_name='stage', action='replace',
                                field_lens='vchall', hova=hova)
                #
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
