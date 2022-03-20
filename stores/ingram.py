from pathlib import Path
import pandas as pd


def ingram_reader(dirpath, hova='19'):
    df_all = pd.DataFrame()
    print("hova: ", hova)
    directory = 'today'
    p = Path(dirpath).joinpath(directory)
    print(p)
    for f in p.iterdir():
        df = pd.read_csv(f, sep='\t', header=0, index_col=None)
        print(df.shape[0])
        df_all = df_all.append(df)
    print(df_all['PTD_pub_comp'].sum())
    print(df_all.shape[0])


def main():
    ingram_reader('h:/NextCloud/Finance/szamitas/2021_12_december/ingram/report', hova='19')


if __name__ == '__main__':
    main()
