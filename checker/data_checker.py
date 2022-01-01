import pandas as pd


def d_checker(df=None, right_length=255):
    if df is None:
        return
    fields = [col for col in df.columns]
    over_the_limit = {}
    temp = pd.DataFrame()
    for field in fields:
        temp[field] = df[field].astype("str")
        m = max(temp[field].str.len())
        if m > right_length:
            over_the_limit[field] = m
    return over_the_limit


if __name__ == '__main__':
    d_checker()
