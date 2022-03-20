from pathlib import Path

import pandas as pd

from engineer import sql_writer as sqw


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


def main(dirpath, hova='19'):
    p = Path(dirpath).joinpath('gardners')
    table = 'stg_fin2_20_gardners'
    for f in p.iterdir():
        print(f)
        if f.name == 'EMCONT0E (1).CSV':
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
            print(df.columns)
            print(df.tail())
            df = df[df['TOTAL-NET-LINE-VALUE'] != '']
            df['TOTAL-NET-LINE-VALUE'] = df['TOTAL-NET-LINE-VALUE'].astype(float)
            print('Gardners: ', df['TOTAL-NET-LINE-VALUE'].sum())
            sqw.write_to_db(df, table, action='replace', hova=hova, field_lens='vchall')


if __name__ == '__main__':
    main('/Users/frank/pd/finance_report/2022_01_january', hova='0')
