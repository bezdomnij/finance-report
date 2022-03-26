from pathlib import Path
from engineer import sql_writer as sqw
import pandas as pd

TABLE = 'stg_fin2_20101_findaway_'
FILENAME = 'Digital Royalty)'
SOURCE_DIR = '2022_02_february'
DATA_DIR = 'findaway'
SUM_FIELD = 'Royalty Payable'


def findaway(dirpath, hova='0'):
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    record_count = 0
    for f in p.iterdir():
        if f.is_file() and f.suffix == '.xlsx' and f.stem[:2] != '~$' and FILENAME in f.stem:
            sheet_names = ['Library', 'Retail', 'Subscription', 'Pool']
            for s in sheet_names:
                df = pd.read_excel(f, sheet_name=s, header=0)
                print(f"{df[SUM_FIELD].sum():-10.2f} {s}, records: {df.shape[0]}")
                record_count += df.shape[0]
                table = TABLE + s.lower()
                sqw.write_to_db(df, table, hova=hova, action='replace', field_lens='vchall')
            print(record_count)


def main():
    # findaway('h:/NextCloud/Finance', hova='0')
    findaway('/Users/frank/pd/Nextcloud', hova='19')


if __name__ == '__main__':
    main()
