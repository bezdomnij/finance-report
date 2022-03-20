from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw


def perlego(dirpath, hova):
    directory = 'perlego'
    table_name = 'stg_fin2_37_perlego'
    df_all = pd.DataFrame()
    p = Path(dirpath).joinpath(directory)
    print(p)
    for f in p.iterdir():
        print(f.stem)
        df = pd.read_csv(f, header=1, encoding='utf-8')
        # print(df.columns)
        df_all = df_all.append(df)
    sqw.write_to_db(df_all, hova=hova, table_name=table_name, field_lens='mindegy')


def main():
    perlego('h:/NextCloud/Finance/2022_01_january', '0')


if __name__ == '__main__':
    main()
