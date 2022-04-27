from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH

TABLE = 'stg_fin2_37_perlego'
FILENAME = 'Sales_Report'
DATA_DIR = 'perlego'
SUM_FIELD = 'royalty_share'


def perlego(hova='0'):
    """
    All perlego files in source directory back to 19. All assembled together and written once to db
    :param dirpath: source dir, sales report
    :param hova: server to write to
    :return: nothing, just action
    get the date from the filename - name files properly!
    """
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    df_all = pd.DataFrame()
    files = [f for f in p.iterdir()]
    files.sort()
    for f in files:
        if f.suffix == '.csv':  # and FILENAME in f.stem:
            df = pd.read_csv(f, encoding='utf-8', header=1)
            df['Date'] = REPORT_MONTH[:4] + '-' + REPORT_MONTH[5:7] + '-15'
            # df['Date'] = f.stem[:4] + '-' + f.stem[4:6] + '-15'
            df[SUM_FIELD] = df[SUM_FIELD].str.strip().str.slice(start=1)

            print(f"{f.stem}\t{round(df[SUM_FIELD].astype('float64').sum(), 2)}\t{df.shape[0]}\trecords")
            df_all = df_all.append(df)

    szumma = df_all[SUM_FIELD].astype('float64').sum()
    print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.2f}\n")
    # df_all.info()
    df_all = df_all.sort_values(by='Date')
    sqw.write_to_db(df_all, TABLE, hova=hova, action='replace', field_lens='vchall')


def main():
    perlego(hova='pd')


if __name__ == '__main__':
    main()
