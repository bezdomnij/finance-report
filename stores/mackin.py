from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

TABLE = 'stg_fin2_36_mackin_data'
FILENAME = 'PUBLISHDRIVE_EBOOKS_2022_'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'mackin'
SUM_FIELD = 'Ext Cost'


def mackin(dirpath, hova='0'):
    """
    ireader sales needs catalog info, sales file has no isbn, just ireader id
    get the isbn from the catalog that has both
    checks structure and sums. Needs extra steps on the sql side to get isbns, some of them missing
    :param dirpath: sales report dir
    :param hova: sever where to write
    :return: nothing
    """
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    for f in p.iterdir():
        if f.suffix in ['.xlsx', '.xls', '.XLS'] and FILENAME in f.stem:
            df = pd.read_excel(f, header=4)
            print(df.columns)
            df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1)
            print(df.shape[0])
            df = df[df['ISBN'].notna()]
            df = df[df['Title'] != 'Title']
            print(df.shape[0])
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}\n")
            sqw.write_to_db(df, TABLE, hova=hova, action='replace', field_lens='vchall')


def main():
    # mackin('/Users/frank/pd/Nextcloud', '0')
    mackin('e:/pd/sales_report', '19')


if __name__ == '__main__':
    main()
