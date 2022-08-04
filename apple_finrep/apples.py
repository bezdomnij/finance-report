import logging
from pathlib import Path
from result import Result
import numpy as np
import pandas as pd

import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATE_FIELD = 'Start Date'
DATE2_FIELD = 'End Date'
DATA_DIR = 'apple'
CURRENCIES = {
    'US': 'USD',
    'CH': 'CHF',
    'NO': 'NOK',
    'NZ': 'NZD',
    'AU': 'AUD',
    'CO': 'COP',
    'CL': 'CLP',
    'CZ': 'CZK',
    'DK': 'DKK',
    'EU': 'EUR',
    'GB': 'GBP',
    'HU': 'HUF',
    'JP': 'JPY',
    'LL': 'USD',
    'SE': 'SEK',
    'PL': 'PLN',
    'PE': 'PEN',
    'RO': 'RON',
    'CA': 'CAD',
    'BR': 'BRL',
    'BG': 'BGN',
    'MX': 'MXN'
}

sum_df = {'file': [], 'r_count': [], 'currency': [], 'sum': [], 'built_in_total': [], 'date_min': [], 'date_max': []}


def read_file_content(c):
    global min_date, max_date
    total = pd.DataFrame()
    aggregated_df = pd.DataFrame()
    if c.is_file():
        location = c.stem.split('_')[-1]
        df = pd.read_csv(c, sep='\t', index_col=None)
        record_count = df.shape[0]
        # print(f"{c.name} record count: ", record_count)
        df['Vendor Identifier'] = df['Vendor Identifier'].astype(str).str.slice(stop=13)
        # print(df['Vendor Identifier'])
        df['Pre-order Flag'].replace({np.NAN: None}, inplace=True)
        sum_df['file'].append(c.stem)
        sum_df['r_count'].append(record_count)
        sum_df['currency'].append((CURRENCIES.get(location, 'nincs')))
        sum_df['sum'].append(round(df["Extended Partner Share"].sum(), 3))
        sum_df['built_in_total'].append(df[df['Start Date'] == 'Total_Amount']['End Date'].iloc[-1])
        df.drop(df.tail(3).index, inplace=True)
        date_borders = util.get_df_dates(DATE_FIELD, 1, df)
        date2_borders = util.get_df_dates(DATE2_FIELD, 1, df)
        min_date = min(date_borders[0], date2_borders[0])
        max_date = max(date_borders[1], date2_borders[1])
        sum_df['date_min'] = min_date
        sum_df['date_max'] = max_date
        aggregated_df = pd.concat([total, df])

    return aggregated_df, (min_date, max_date)


def find_am(sor):
    try:
        amount = float(sor[-2][1:-1])
    except ValueError as e:
        print(f"{e}: {sor}")
        return 0
    else:
        return amount


def read_sum_file(sum_file):
    total_usd = 0
    try:
        with sum_file.open(mode='r') as sums:
            for line in sums.readlines():
                sor = line.rstrip()
                sor2 = sor.split(',')[:-1]
                total_usd += find_am(sor2)
    except FileNotFoundError as e:
        print(f"No summary report, return 0,\n{e}")
    return round(total_usd, 3)


def read_apple(hova=HOVA):
    global date_borders
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    sum_file = p.joinpath('financial_report.csv')
    total_df = pd.DataFrame()
    files = util.get_file_list(p)
    grand_total = read_sum_file(sum_file)
    gt = grand_total if grand_total != 0 else "dunno. summary file is not there."
    try:
        print(f"Total USD: {gt:12,.2f}")
    except ValueError:
        print("Summary file is not there.")
    # sum_df = pd.read_csv(sum_file, header=2, encoding='utf-8')
    # sum_df.info()
    # template_df = pd.read_csv(files[0], sep='\t', index_col=None)
    # total = pd.DataFrame(columns=[x for x in template_df.columns], index=None)  # collective df
    if len(files) > 0:
        for f in files:
            if f.suffix == '.txt':
                ret_value = read_file_content(f)
                date_borders = ret_value[1]
                total_df = pd.concat([total_df, ret_value[0]])
        sqw.write_to_db(total_df, 'stg_fin2_1_apple', action='replace', hova=hova, field_lens='vchall')
        print("EXTENDED PARTNER SHARE", total_df['Extended Partner Share'].sum())
        print("UNITS SOLD", int(total_df['Quantity'].sum()))
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {total_df.shape[0]} records\n")
        res.append(Result(DATA_DIR.upper(), REPORT_MONTH,
                          total_df.shape[0], 'USD', '', grand_total, date_borders[0], date_borders[1]))
        return pd.DataFrame(sum_df, index=range(1, 23)), res
        # return pd.DataFrame(sum_df, index=None)
    else:
        util.empty(DATA_DIR)


def apple(hova=HOVA):
    try:
        resultset_df, res = read_apple(hova=hova)
    except TypeError as e:
        print(f"{e} no Excel can be made")
        return []
    # all txt files result - writing to Excel
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    resultset_df.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
    workbook = writer.book
    worksheet1 = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    f3 = workbook.add_format({'align': 'right'})
    worksheet1.set_column('B:B', None, format1)
    worksheet1.set_column('D:D', None, format1)
    worksheet1.set_column('C:C', None, f3)

    # Auto-adjust columns' width - writing to Excel
    for column in resultset_df:
        column_width = max(resultset_df[column].astype(str).map(len).max() + 4, len(column))
        col_idx = resultset_df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

    writer.save()
    return res


def main():
    apple('19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='../logs/datacamp.log', filemode='w')
    main()
