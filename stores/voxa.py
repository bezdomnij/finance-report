from pathlib import Path
import pandas as pd
from result import Result
import util
from engineer import sql_writer as sqw
from config import MAIN_DIR, REPORT_MONTH, HOVA

TABLE = 'stg_fin2_49_voxa'
FILENAME = 'Raport 202'
DATA_DIR = 'voxa'
SUM_FIELD = 'Pret net cu TVA (RON)'
DATE_FIELD = 'Data vanzarii'


def voxa(hova=HOVA):
    """
    ireader sales needs catalog info, sales file has no isbn, just ireader id
    get the isbn from the catalog that has both
    checks structure and sums. Needs extra steps on the sql side to get isbns, some of them missing
    :param hova: sever where to write
    :return: nothing
    """
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    if len(files) > 0:
        print(p)
        df_all = pd.DataFrame()
        record_count, szumma = 0, 0
        for f in files:
            if f.suffix == '.csv' and FILENAME in f.stem:  # .csv!!!
                df = pd.read_csv(f, encoding='utf-8', header=0)
                rc = df.shape[0]
                szm = round(df[SUM_FIELD].sum(), 3)
                record_count += rc
                szumma += szm
                df_all = df_all.append(df)
                print(f.name, rc, szm)
        date_borders = util.get_df_dates(DATE_FIELD, 5, df_all)
        sqw.write_to_db(df_all, TABLE, action='replace', hova=hova, field_lens='vchall')
        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.3f}\n")
        res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                          'RON', '', szumma, date_borders[0], date_borders[1]))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    voxa(hova='19')


if __name__ == '__main__':
    main()
