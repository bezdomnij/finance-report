from config import MAIN_DIR, REPORT_MONTH, HOVA
from pathlib import Path
import pandas as pd
import util
from engineer import sql_writer as sqw

DIRECTORY = 'audible'
SUM1_FIELD = 'Total Royalties'
SUM2_FIELD = 'Total Royalties'
TABLE1 = 'stg_fin2_20103_audible'
TABLE2 = 'stg_fin2_20103_audible_subs'


def audible(hova=HOVA):
    todo_sheets = ['SalesDetails', 'On-Demand Royalty Bearing']
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DIRECTORY)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            if f.is_file() and f.suffix in ('.xlsx', '.xls') and f.stem[:2] != '~$':
                for s in todo_sheets:
                    if s == 'SalesDetails':
                        df = pd.read_excel(f, sheet_name=s, header=3)
                        df = df.drop(df[df['Parent Product ID'] == 'Grand Total'].index)
                        total1 = df[SUM1_FIELD].sum()
                        print(total1)
                        sqw.write_to_db(df, TABLE1, hova=hova, field_lens='vchall')
                    elif s == 'On-Demand Royalty Bearing':
                        df = pd.read_excel(f, sheet_name=s, header=2)
                        df = df.drop(df[df['Product ID'] == 'Earner Total'].index)
                        df = df.drop(df[df['Product ID'] == 'Grand Total'].index)
                        total2 = df[SUM2_FIELD].sum()
                        print(total2)
                        sqw.write_to_db(df, TABLE2, hova=hova, field_lens='vchall')

    else:
        util.empty(DIRECTORY)


def main():
    audible(hova='pd')


if __name__ == '__main__':
    main()
