"""
multiple sources - two Excels, each file with one sheet only
multiple destinations - two tables
- header line location identical
- sum field identical: FIELD
- need to drop rows below data
"""
from datetime import datetime, date
from pathlib import Path
import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from result import Result
import pandas as pd

TABLE_1 = 'stg_fin2_33_odilo_ppu'
TABLE_2 = 'stg_fin2_33_odilo_agency'
FILENAME_1 = '_PublishDrive_PPU_Sales_Report'
FILENAME_2 = '_PublishDrive_Sales_Report'
DATA_DIR = 'odilo'
SUM_FIELD = 'Totals (USD)'
DATE_FIELD = 'Date'


# SUM_FIELD = 'Totals'  # valamelyik


def get_dates_from_filename(stem):
    parts = stem.split('_')
    year = int(parts[2])
    month = datetime.strptime(parts[1], '%B').month
    last_day = util.MAX_DAYS[month]
    return date(year, month, 1), date(year, month, last_day)


def odilo(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    szumma = 0
    record_count = 0
    print(p)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            print(f)
            r, s = 0, 0
            if f.is_file() and (f.suffix == '.xlsx' or f.suffix == '.xls') and f.stem[:2] != '~$':
                if FILENAME_1 in f.stem:
                    r, s = util.get_content_xl_onesheet(f, TABLE_1, hova=hova, sum_field=SUM_FIELD
                                                        , na_field='Title', header=0, sheet_name='')
                    # (file, table, hova, sum_field, na_field, header=0, sheet_name='')
                    dates = get_dates_from_filename(f.stem)
                    print(dates)
                    res.append(Result(DATA_DIR.upper(), REPORT_MONTH, r,
                                      'USD', 'PPU', s, dates[0], dates[1]))
                if FILENAME_2 in f.stem:
                    r, s = util.get_content_xl_onesheet(f, TABLE_1, hova=hova, sum_field=SUM_FIELD
                                                        , na_field='Title', header=0, sheet_name='')
                    df = pd.read_excel(f, header=1, index_col=None)
                    print(df.columns)
                    df = df[df['Title'].notna()]
                    date_borders = util.get_df_dates(DATE_FIELD, 6, df)
                    print(date_borders)
                    res.append(Result(DATA_DIR.upper(), REPORT_MONTH, r,
                                      'USD', 'Retail', s, date_borders[0], date_borders[1]))
                record_count += r
                szumma += s

        print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count:10,d} records, total: {szumma:-10,.2f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    odilo(hova='19')


if __name__ == '__main__':
    main()
