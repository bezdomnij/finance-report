from pathlib import Path
from engineer import sql_writer as sqw
import pandas as pd

SOURCE_DIR = '2022_02_february'
DATA_DIR = 'findaway'
TABLE = 'stg_fin2_20101_findaway_'


def findaway(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)

    for f in p.iterdir():
        if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$':
            sheet_names = ['Library', 'Retail', 'Subscription', 'Pool']
            for s in sheet_names:
                df = pd.read_excel(f, sheet_name=s, header=0)
                print(f"{df['Royalty Payable'].sum():-10.2f} {s}")
                table = TABLE + s.lower()
                sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')


def main():
    findaway('h:/NextCloud/Finance', hova='0')


if __name__ == '__main__':
    main()
