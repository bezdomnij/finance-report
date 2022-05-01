from pathlib import Path
import pandas as pd

import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_rts2_06_ekonyv'
FILENAME = '-ekonyv-fogyas'
DATA_DIR = 'ekönyv'
SUM_FIELD = 'Nettó fizetendő'


def ekonyv(hova=HOVA):
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files = util.get_latest_file(files, '.xlsx')
        for f in files:
            if f.is_file() and f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
                # df = pd.read_excel(f, sheet_name='PublishDrive', header=12)
                df = pd.read_excel(f, header=12)
                df.rename(columns={'Cím ': 'Cím'}, inplace=True)  # NON-STANDARD: remove space from field name

                df = df[df['ISBN'].notna()]  # drop lines below data
                df['ISBN'] = df['ISBN'].astype('int64')  # otherwise, a .0 is put to the end
                record_count = df.shape[0]
                # print(f"Összesen ekönyv: {round(df['Nettó fizetendő'].sum(), 2)}")
                sqw.write_to_db(df, TABLE, hova=hova, action='replace', field_lens='vchall')
                szumma = df[SUM_FIELD].sum()
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.0f}\n")
    else:
        util.empty(DATA_DIR)


def main():
    ekonyv('0')


if __name__ == '__main__':
    main()
