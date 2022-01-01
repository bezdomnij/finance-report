import re


def check_file_name(fname, type):
    parts = fname.split('-')
    if len(parts) != 5 and type == 'g':
        print(f"The number of name-parts is off: {parts}")
        return 0
    if parts[0] != 'GoogleEarningsReport':
        print('Not a Google earnings report?')
        return 0
    if type == 'a':
        return 1
    pattern = r"^[2][0][1-2][0-9]$"
    year = re.compile(pattern)
    if not re.match(year, parts[1]):
        print(f'The year part is off: {parts[1]}')
        return 0
    pattern = r"^[0-2][0-9]$"
    month = re.compile(pattern)
    if not re.match(month, parts[2]):
        print(f'The month part is off: {parts[2]}')
        return 0
    if not parts[3] == 'PD':
        print(f'Not a regular PD Google earnings file, 4th part is not `PD`: {parts[3]}')
        return 0
    if not len(parts[4]) == 13:
        print(f'Last part is not 13 in length: {parts[4]}')
        return 0
    return 1


def main():
    print("main")


if __name__ == '__main__':
    main()
