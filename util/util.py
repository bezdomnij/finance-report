import logging
import re


def get_period(fname):
    g_pattern = r'202[0-2]-[0-1][0-9]'
    prog = re.compile(g_pattern)
    return prog.findall(fname)


def check_google_file_name(fname):
    result = get_period(fname)
    name_and_extension = fname.split('.')
    if 'GoogleEarningsReport' in name_and_extension[0] and name_and_extension[1] == 'csv':
        name_parts = name_and_extension[0].split('_')  # gg-nel nincs benne _
        period = tuple(get_period(fname)[0].split('-'))
        if len(period) > 0:
            if len(name_parts) == 2:  # ilyen a GoogleAudio
                result = ('ga', period)
            elif len(name_parts) == 1:
                result = ('gg', period)
            else:
                print("Filename is not ok, too many parts (sep='_')")
                return None, period
        else:
            period = (0, 0)
        if period[0] == 0 or period[1] == 0:
            print("Don't know the period of filename.")
            return None, period
    else:
        print("Does not appear to be a Google earnings .csv report.")
    return result


def check_incoming(f):
    ftype, period = check_google_file_name(f.name)
    print(ftype, period)
    return ftype, period


def main():
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    # check_file_name("GoogleEarningsReport_whatever.csv")
    check_google_file_name("GoogleEarningsReport_2021-11.csv")


if __name__ == '__main__':
    main()
