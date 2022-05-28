from config import MAIN_DIR, REPORT_MONTH, HOVA
from pathlib import Path
import pandas as pd
import util
from result import Result
from engineer import sql_writer as sqw
import re
from datetime import datetime

DATA_DIR = 'audible'
SUM1_FIELD = 'Total Royalties'
SUM2_FIELD = 'Total Royalties'
TABLE1 = 'stg_fin2_20103_audible'
TABLE2 = 'stg_fin2_20103_audible_subs'
DATES = {
    'Q_1': (1, 1, 3, 31),
    'Q_2': (4, 1, 6, 30),
    'Q_3': (7, 1, 9, 30),
    'Q_4': (10, 1, 12, 31)
}


def get_dates(stem):
    pattern = r"\bACCT_PublishDrive__Inc.__US_QUARTERLY_(Q_[1-4])_(202[2-9]$)"
    p = re.compile(pattern)
    m = re.match(p, stem)
    q = m.group(1)
    y = int(m.group(2))
    begin = datetime(y, DATES[q][0], DATES[q][1]).date()
    end = datetime(y, DATES[q][2], DATES[q][3]).date()
    return begin, end


def audible(hova=HOVA):
    res = []
    todo_sheets = ['SalesDetails', 'On-Demand Royalty Bearing']
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            szumma, record_count = 0.00, 0
            if f.is_file() and f.suffix in ('.xlsx', '.xls') and f.stem[:2] != '~$':
                dates = get_dates(f.stem)
                for s in todo_sheets:
                    df = pd.DataFrame()
                    szm, rc = 0.00, 0
                    if s == 'SalesDetails':
                        df = pd.read_excel(f, sheet_name=s, header=3)
                        df = df.drop(df[df['Parent Product ID'] == 'Grand Total'].index)
                        szm = df[SUM1_FIELD].sum()
                        rc = df.shape[0]
                        sqw.write_to_db(df, TABLE1, hova=hova, field_lens='vchall')

                    elif s == 'On-Demand Royalty Bearing':
                        df = pd.read_excel(f, sheet_name=s, header=2)
                        df = df.drop(df[df['Product ID'] == 'Earner Total'].index)
                        df = df.drop(df[df['Product ID'] == 'Grand Total'].index)
                        szm = df[SUM2_FIELD].sum()
                        rc = df.shape[0]
                        sqw.write_to_db(df, TABLE2, hova=hova, field_lens='vchall')

                    print(f"{DATA_DIR} sheet: {s} | {REPORT_MONTH}, {rc:10,d} records, total: {szm:-10,.2f}")
                    record_count += rc
                    szumma += szm
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                  'USD', '', szumma, dates[0], dates[1]))

    else:
        util.empty(DATA_DIR)

    return res


def main():
    audible(hova='0')


if __name__ == '__main__':
    main()
