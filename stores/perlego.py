from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util

TABLE = 'stg_fin2_37_perlego'
FILENAME = 'Sales_Report'
DATA_DIR = 'perlego'
SUM_FIELD = 'royalty_share'
OFFSET = -1


def perlego(hova=HOVA):
    """
    All perlego files in source directory back to 19. All assembled together and written once to db
    :param hova: server to write to
    :return: nothing, just action
    get the date from the filename - name files properly!
    """
    print(REPORT_MONTH)
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    df_all = pd.DataFrame()
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files.sort()
        for f in files:
            if f.suffix == '.csv':  # and FILENAME in f.stem:
                df = pd.read_csv(f, encoding='utf-8', header=1)
                base_date = REPORT_MONTH
                if OFFSET != 0:
                    base_date = util.set_date(REPORT_MONTH, OFFSET)
                df['Date'] = base_date[:4] + '-' + base_date[5:7] + '-15'
                df[SUM_FIELD] = df[SUM_FIELD].str.strip().str.slice(start=1)
                print(f"{f.stem}\t{round(df[SUM_FIELD].astype('float64').sum(), 2)}\t{df.shape[0]}\trecords")
                df_all = df_all.append(df)

        szumma = df_all[SUM_FIELD].astype('float64').sum()
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, total: {szumma:-10,.2f}\n")
        print(df_all.tail())
        df_all = df_all.sort_values(by='Date')
        sqw.write_to_db(df_all, TABLE, hova=hova, action='replace', field_lens='vchall')
    else:
        print(f"Looks like the `{DATA_DIR}` directory is empty.")


def main():
    perlego(hova='19')


if __name__ == '__main__':
    main()
