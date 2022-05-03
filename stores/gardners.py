from pathlib import Path

import pandas as pd
from result import Result
import util
from config import MAIN_DIR, REPORT_MONTH, HOVA
from engineer import sql_writer as sqw

DATA_DIR = 'gardners'
SUM_FIELD = 'TOTAL-NET-LINE-VALUE'
TABLE = 'stg_fin2_20_gardners'
FILENAME = 'EMCONT0E'


def find_bad_comma(line, positions):
    one, two, three = '', '', ''
    for i in range(len(positions) // 2):
        try:
            one = line[positions[0]:positions[1] + 1]
            two = line[positions[2]:positions[3] + 1]
            three = line[positions[4]: positions[5] + 1]
        except IndexError:
            continue
    new_one, new_two, new_three = forget_comma(one, two, three)
    if one != new_one:
        line = line.replace(one, new_one)
    if two != new_two:
        line = line.replace(two, new_two)
    if three != new_three:
        line = line.replace(three, new_three)
    return line


def forget_comma(one, two, three):
    temp1 = one.replace('"', '')
    temp2 = two.replace('"', '')
    temp3 = three.replace('"', '')
    return temp1.replace(',', ';'), temp2.replace(',', ';'), temp3.replace(',', ';')


def gardners(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)
    if files is None:
        return
    if len(files) > 0:
        for f in files:
            print(f)
            if f.is_file() and FILENAME in f.stem and f.suffix in ('.csv', '.CSV'):
                with open(f, mode='r') as g:
                    contents = g.readlines()
                    header = contents[0].rstrip().split(',')
                    df = pd.DataFrame(columns=header, index=None)
                    for ln in contents[1:]:
                        line = ln.rstrip()
                        positions = [pos for pos, char in enumerate(line) if char == '"']
                        if len(positions) > 0:
                            line = find_bad_comma(line, positions)
                        item = dict(zip(header, line.split(',')))
                        df = df.append(item, ignore_index=True)
                df = df[df[SUM_FIELD] != '']
                df[SUM_FIELD] = df[SUM_FIELD].astype(float)
                szumma = df[SUM_FIELD].sum()
                record_count = df.shape[0]
                sqw.write_to_db(df, TABLE, action='replace', hova=hova, field_lens='vchall')
                print(f"{DATA_DIR.upper()} | {REPORT_MONTH}, {record_count} records, total: {szumma:-10,.2f}\n")
                res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count, 'GBP', '', szumma))
    else:
        util.empty(DATA_DIR)
    return res


def main():
    gardners(hova='0')


if __name__ == '__main__':
    main()

