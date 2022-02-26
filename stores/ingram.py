import pandas as pd
from pathlib import Path


def ingram_old(dirpath):
    df_all = pd.DataFrame()
    p = Path(dirpath).joinpath('ingram_before')
    for f in p.iterdir():
        if f.suffix == '.csv':
            print(f)


def main():
    ingram_old('/Users/frank/pd/sales_report/ingram_lightningsource')


if __name__ == '__main__':
    main()
