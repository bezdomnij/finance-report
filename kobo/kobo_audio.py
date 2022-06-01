"""
df2 = df.rename({
                ' Read Period ': 'Read Period',
                ' Publisher name ': 'Publisher name',
                ' eISBN ': 'eISBN',
                ' Author ': 'Author',
                ' Title ': 'Title',
                ' List price (TaxIn) ': 'List price (TaxIn)',
                ' List price (TaxOut) ': 'List price (TaxOut)',
                ' List price currency ': 'List price currency',
                ' Region ': 'Region',
                ' Read threshold (%) ': 'Read threshold (%)',
                ' Reads ': 'Reads',
                ' Total payable ': 'Total payable',
                ' Foreign exchange to payable currency ': 'Foreign exchange to payable currency',
                ' Total in payable currency ': 'Total in payable currency',
                ' Payable Currency ': 'Payable Currency',
                ' Value Per Minute ': 'Value Per Minute',
                ' Total Minutes ': 'Total Minutes',
                ' Revenue earned per title ': 'Revenue earned per title',
                ' Publisher revenue share (%) ': 'Publisher revenue share (%)',
                ' Total publisher revenue share in payable currency ($) ': 'Total publisher revenue share in payable currency ($)'
                }, axis=1)
"""

from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result

TABLE = 'stg_fin2_20002_kobo_audio'
FILENAME = 'Content 2 Connect Audio_CONTENT2CONNECT_AUDIO_'
DATA_DIR = 'kobo audio'
SUM_FIELD = 'Net Due (Payable Currency)'
DATE_FIELD = 'Date'


def kobo_audio(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for file in p.iterdir():
            if file.stem[:2] != '~$' and 'sub' not in file.stem.lower():
                df = pd.read_excel(file, sheet_name='Details', header=0)
                szumma = df[SUM_FIELD].sum()
                record_count = df.shape[0]
                print(file.stem)
                date_borders = util.get_df_dates(DATE_FIELD, 3, df)
                print(date_borders)
                sqw.write_to_db(df, TABLE, hova=hova, field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                  'USD', '', szumma, date_borders[0], date_borders[1]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    kobo_audio(hova='pd')


if __name__ == '__main__':
    main()
