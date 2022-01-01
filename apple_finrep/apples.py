from pathlib import Path

import pandas as pd

currencies = {
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

sum_df = {'file': [], 'r_count': [], 'currency': [], 'sum': [], 'built_in_total': []}


def read_file_content(c, total):
    location = c.stem.split('_')[-1]
    df = pd.read_csv(c, sep='\t')
    record_count = df.shape[0]
    print()

    sum_df['file'].append(c.stem)
    sum_df['r_count'].append(record_count)
    sum_df['currency'].append((currencies.get(location, 'nincs')))
    sum_df['sum'].append(round(df["Extended Partner Share"].sum(), 3))
    sum_df['built_in_total'].append(df[df['Start Date'] == 'Total_Amount']['End Date'].iloc[-1])
    aggregated_df = pd.concat([total, df], ignore_index=True)
    return aggregated_df


def read_apple(dir_path):
    p = Path(dir_path)
    files = [f for f in p.iterdir()]
    template_df = pd.read_csv(files[0], sep='\t')
    total = pd.DataFrame(columns=[x for x in template_df.columns])

    for c in p.iterdir():
        if c.suffix != '.csv':
            total = read_file_content(c, total)

    print("EXTENDED PARTNER SHARE", total['Extended Partner Share'].sum())
    print("UNITS SOLD", int(total['Quantity'].sum()))
    print(total.shape[0])
    return pd.DataFrame(sum_df, index=range(1, 23))


def main():
    dir_path = '/Users/frank/pd/finance_report/apple'
    resultset_df = read_apple(dir_path)
    print(resultset_df)

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    resultset_df.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
    workbook = writer.book
    worksheet1 = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    f3 = workbook.add_format({'align': 'right'})
    worksheet1.set_column('B:B', None, format1)
    worksheet1.set_column('D:D', None, format1)
    worksheet1.set_column('C:C', None, f3)

    # Auto-adjust columns' width
    for column in resultset_df:
        column_width = max(resultset_df[column].astype(str).map(len).max() + 4, len(column))
        col_idx = resultset_df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

    writer.save()


if __name__ == '__main__':
    main()
