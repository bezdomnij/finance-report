from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from result import Result

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
    res = []
    # print(REPORT_MONTH)
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    df_all = pd.DataFrame()
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        files.sort()
        record_count = 0
        for f in files:
            if f.suffix == '.csv':  # and FILENAME in f.stem:
                df = pd.read_csv(f, encoding='utf-8', header=1)
                base_date = REPORT_MONTH
                if OFFSET != 0:
                    base_date = util.set_date(REPORT_MONTH, OFFSET)
                df['Date'] = base_date[:4] + '-' + base_date[5:7] + '-15'
                df[SUM_FIELD] = df[SUM_FIELD].str.strip().str.slice(start=1)
                rc = df.shape[0]
                szm = df[SUM_FIELD].astype('float64').sum()
                print(f"{f.stem} |\t{rc} records, {round(szm, 2)}")
                df_all = df_all.append(df)
                record_count += rc

        szumma = df_all[SUM_FIELD].astype('float64').sum()
        sqw.write_to_db(df_all, TABLE, hova=hova, action='replace', field_lens='vchall')
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
        res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'USD', '', szumma))
        # print(df_all.tail())
        # print()
        # df_all = df_all.sort_values(by='Date')
    else:
        util.empty(DATA_DIR)
    return res


def main():
    perlego(hova='pd')


if __name__ == '__main__':
    main()
