from pathlib import Path
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH
import util
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_rts2_09_multimediaplaza'
FILENAME = 'Kossuth'
SOURCE_DIR = REPORT_MONTH
DATA_DIR = 'Multimediaplaza'
SUM_FIELD = 'jogdij'


def multimediaplaza(hova='0'):  # undecided: TOGETHER OR SEPARATELY, BECAUSE SOURCE FILE CONTAINS BOTH
    collect_df = pd.DataFrame()
    res = []
    p = Path(MAIN_DIR).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    record_count, szumma = 0, 0
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            # if f.is_file() and f.suffix == '.csv' and FILENAME in f.stem:
            #     df = pd.read_csv(f, header=0, sep=',', index_col=None)
            #     df.dropna(how='all', axis=1, inplace=True)
            #     df.drop(df.tail(1).index, inplace=True)
            #     df['jogdij'] = df['jogdij'].replace(',', '.')
            #     rc = df.shape[0]
            #     record_count += rc
            #     szm = df['jogdij'].sum()
            #     szumma += szm
            #     collect_df = collect_df.append(df)
            #     print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
            #           f"total: {szumma:-10,.2f}\t, {record_count} records")
            #     sqw.write_to_db(collect_df, TABLE, db_name='stage', field_lens='mas', action='replace',
            #                     hova=hova)
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$':
                df = pd.read_excel(f, header=0, index_col=None)
                df.dropna(how='all', axis=1, inplace=True)
                df['jogdij'] = df['jogdij'].replace(',', '.')
                df.drop(df.tail(1).index, inplace=True)
                rc = df.shape[0]
                record_count += rc
                szm = df['jogdij'].sum()
                szumma += szm
                collect_df = collect_df.append(df)
                # print(df)
                print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
                      f"total: {szumma:-10,.2f}\t, {record_count} records\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'HUF', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    multimediaplaza(hova='0')


if __name__ == '__main__':
    main()
