import csv
from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw


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
                df = pd.DataFrame(columns=header)
                for l in contents[1:]:
                    line = l.rstrip()
                    try:
                        positions = [pos for pos, char in enumerate(line) if char == '"']
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
                    item = dict(zip(header, line.split(',')))
                    df = df.append(item, ignore_index=True)
            print(df.columns)
            print(df.tail())
            df['TOTAL-NET-LINE-VALUE'] = df['TOTAL-NET-LINE-VALUE'].astype(float)
            print(df['TOTAL-NET-LINE-VALUE'].sum())
            sqw.write_to_db(df, table, action='replace', hova=hova, field_lens='mindegy')


if __name__ == '__main__':
    main('/Users/frank/pd/sales_report')
