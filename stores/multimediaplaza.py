from pathlib import Path
import pandas as pd
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from engineer import sql_writer as sqw
from result import Result

TABLE = 'stg_fin2_9_multimediaplaza'
FILENAME = 'Kossuth'
DATA_DIR = 'Multimediaplaza'
SUM_FIELD = 'jutalek'


def multimediaplaza(hova=HOVA):
    """
    able to handle and lump together multiple source files
    March is made from Excel, normally it's .csv
    :param hova: lokalisan is indithato masik cellal
    :return: Result object
    """
    collect_df = pd.DataFrame()
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    record_count, szumma = 0, 0
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$':
                df = pd.read_excel(f, header=0, index_col=None)
                df = df.drop(df[df['dátum'] == 'Összesen:'].index)
                df[SUM_FIELD] = df[SUM_FIELD].replace(',', '.')
                rc = df.shape[0]
                szm = df[SUM_FIELD].sum()
                record_count += rc
                szumma += szm
                collect_df = collect_df.append(df)
                print(df)
            if not collect_df.empty:
                sqw.write_to_db(collect_df, TABLE, hova=hova, field_lens='vchall')
                print(f"{DATA_DIR.upper()}, file: {f.stem},\t, report: {REPORT_MONTH}, "
                      f"total: {szumma:-10,.2f}\t, {record_count} records\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'HUF', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    multimediaplaza(hova='pd')


if __name__ == '__main__':
    main()
