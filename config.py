from pathlib import Path

# REPORT_MONTH = '2022_04_april'
# REPORT_MONTH = '2022_05_may'
# REPORT_MONTH = '2022_06_june'
# REPORT_MONTH = '2022_07_july'
# REPORT_MONTH = '2022_08_aug'
# REPORT_MONTH = '2022_09_sep'
# REPORT_MONTH = '2022_10_oct'
REPORT_MONTH = '2022_11_nov'


def get_main_dir():
    where_we_are = str(Path.home())
    if 'Yondu' in where_we_are:
        return 'h:/NextCloud/Finance/szamitas'
    elif 'Attila' in where_we_are:
        return 'd:/NextCloud/Finance/szamitas'
    elif 'frank' in where_we_are:
        return '/Users/frank/pd/Nextcloud/szamitas'
    else:
        return 'new_place'


MAIN_DIR = get_main_dir()
HOVA = '19'

if __name__ == '__main__':
    get_main_dir()
