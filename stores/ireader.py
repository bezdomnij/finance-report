from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw

TABLE = 'stg_rts2_46_ireader'
FILENAME = 'PublishDrive_Monthly Sales Detail Data@202202'
SOURCE_DIR = '2022_02_february'
REPORT_MONTH = '2022_02_february'
DATA_DIR = 'ireader'
SUM_FIELD = 'Sharing Amount'


def ireader(dirpath, hova='0'):
    """
    ireader sales needs catalog info, sales file has no isbn, just ireader id
    get the isbn from the catalog that has both
    checks structure and sums. Needs extra steps on the sql side to get isbns, some of them missing
    :param dirpath: sales report dir
    :param hova: sever where to write
    :return: nothing
    """
    p = Path(dirpath).joinpath(SOURCE_DIR).joinpath(DATA_DIR)
    # disable chained assignments
    pd.options.mode.chained_assignment = None
    for f in p.iterdir():
        if f.suffix == '.csv' and FILENAME in f.stem:  # .csv!!!
            df = pd.read_csv(f, encoding='utf-8', header=0)
            # print(f.name)
            # print(df.columns)
            print(df.shape[0], 'records')
            szumma = df[SUM_FIELD].sum()
            print(f"{DATA_DIR}, {REPORT_MONTH}, total: {szumma:-10,.3f}\n")
            sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')
        # elif 'Work' in f.stem:
        #     dfc = pd.read_csv(f, header=0, encoding='utf-8', index_col=None)
        #     cols = list(dfc.columns)
        #     print(f)
        #     print(cols)
        #     dfc = dfc.fillna(0)
        #     dfc['ISBN'] = dfc['ISBN'].astype('int64').astype('str')
        #     # dfc['ISBN'] = dfc['ISBN'].astype("str")
        #     dfc2 = dfc[['ID', 'Title', 'Author', 'ISBN', 'Format']]
        #     dfc2.info()
        #     # sqw.write_to_db(dfc2, 'ireader_cat', hova=hova)


def main():
    # ireader('/Users/frank/pd/Nextcloud', hova='0')
    ireader('h:/Nextcloud/Finance/szamitas', hova='0')


if __name__ == '__main__':
    main()
