from pathlib import Path

# REPORT_MONTH = '2021_11_november'
# REPORT_MONTH = '2021_12_december'
# REPORT_MONTH = '2022_01_january'
# REPORT_MONTH = '2022_02_february'
# REPORT_MONTH = '2022_03_march'
# REPORT_MONTH = '2022_04_april'
# REPORT_MONTH = '2022_05_may'
REPORT_MONTH = '2022_06_june'


# REPORT_MONTH = '2022_07_july'


# MAIN_DIR = '/Users/frank/pd/Nextcloud'
# MAIN_DIR = '/Users/frank/pd/sales_report'
# MAIN_DIR = 'e:/pd/sales_report'


def get_main_dir():
    where_we_are = str(Path.home())
    if 'Yondu' in where_we_are:
        # return 'e:/pd/sales_report'
        return 'h:/NextCloud/Finance/szamitas'
    elif 'frank' in where_we_are:
        return '/Users/frank/pd/Nextcloud/szamitas'
    else:
        return 'new_place'


MAIN_DIR = get_main_dir()
HOVA = 'pd'

if __name__ == '__main__':
    get_main_dir()
