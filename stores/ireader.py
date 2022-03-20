from pathlib import Path
import pandas as pd


def ireader(dirpath, hova='19'):
    df_all = pd.DataFrame()
    print("hova: ", hova)
    directory = 'ireader'
    p = Path(dirpath).joinpath(directory)
    print(p)
    for f in p.iterdir():
        df = pd.read_csv(f, encoding='utf-8', header=0, index_col=None)
        print(df.columns, df.shape[0])
        print(df['Sharing Amount'].sum())
        df_all = df_all.append(df)
    print(df_all['Sharing Amount'].sum())


def main():
    ireader('h:/NextCloud/Finance/szamitas/2021_12_december', hova='19')


if __name__ == '__main__':
    main()
