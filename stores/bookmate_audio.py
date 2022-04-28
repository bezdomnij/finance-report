from pathlib import Path
import util
from engineer import sql_writer as sqw
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH

TABLE = 'stg_fin2_20032_bookmate_audio'
FILENAME = 'PublishDrive__Content_2_Connect__Audio_'
# SOURCE_DIR = REPORT_MONTH
SOURCE_DIR = '2022_05_may'
DATA_DIR = 'bookmate audio'
SUM_FIELD = 'Converted Revenue'


def bookmate_audio(hova='0'):
    p = Path(MAIN_DIR).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files:
        for f in files:
            if f.is_file() and f.suffix in ('.xls', '.xlsx', '.XLS') and FILENAME in f.stem and f.stem[:2] != '~$':
                df = pd.read_excel(f, header=0, index_col=None)
                new_cols = [col.strip() for col in df.columns]
                cols_map = dict(zip(df.columns, new_cols))
                df.rename(columns=cols_map, inplace=True)
                df = df.drop(df[df['Book title'] == 'Grand total:'].index)
                # df = df[df['EAN'].notna()]
                df['sale_date'] = REPORT_MONTH[:4] + '-' + REPORT_MONTH[5:7] + '-15'
                szumma = df[SUM_FIELD].sum()
                record_count = df.shape[0]
                print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
                      f"total: {szumma:-10,.2f}\t, {record_count} records")
                sqw.write_to_db(df, TABLE, db_name='stage', action='replace', field_lens='vchall', hova=hova)


def main():
    bookmate_audio(hova='19')


if __name__ == '__main__':
    main()
