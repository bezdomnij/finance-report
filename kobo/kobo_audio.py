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
from engineer import sql_writer as sqw

TABLE = 'stg_rts2_20002_kobo_audio'
FILENAME = 'Content 2 Connect Audio_CONTENT2CONNECT_AUDIO_Feb 2022'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'kobo audio'
SUM_FIELD = 'Net Due (Payable Currency)'


def kobo_audio(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    for file in p.iterdir():
        if file.stem[:2] != '~$' and 'Sub' not in file.stem:
            df = pd.read_excel(file, sheet_name='Details', header=0)
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}")
            print(df.shape[0], 'records')
            sqw.write_to_db(df, TABLE, hova=hova, field_lens='vchall')


def main():
    kobo_audio('h:/NextCloud/Finance/szamitas', hova='0')
    # kobo_audio('/Users/frank/pd/Nextcloud', hova='0')


if __name__ == '__main__':
    main()
