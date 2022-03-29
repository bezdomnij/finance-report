from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

TABLE = 'stg_rts2_06_ekonyv'
FILENAME = '-ekonyv-fogyas'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'ekönyv'
SUM_FIELD = 'Nettó fizetendő'


def ekonyv_rw(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    for f in p.iterdir():
        if f.is_file() and f.suffix == '.xlsx' and FILENAME in f.stem and f.stem[:2] != '~$':
            df = pd.read_excel(f, sheet_name='PublishDrive', header=12)
            df.rename(columns={'Cím ': 'Cím'}, inplace=True)  # NON-STANDARD: remove space from field name
            df = df[df['ISBN'].notna()]  # drop lines below data
            df['ISBN'] = df['ISBN'].astype('int64')  # otherwise, a .0 is put to the end
            print(f"{df.shape[0]} db, Összesen ekönyv: {round(df['Nettó fizetendő'].sum(), 2)}")
            sqw.write_to_db(df, TABLE, hova=hova, action='replace', field_lens='vchall')
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}\n")


def main():
    # ekonyv_rw('/Users/frank/pd/Nextcloud', '0')
    ekonyv_rw('h:/Nextcloud/Finance/szamitas', '0')


if __name__ == '__main__':
    main()
