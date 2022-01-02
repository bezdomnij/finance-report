import sys
from pathlib import Path

from checker.name_checker import check_file_name


def g_checker(p, type='g'):
    filename_ok = 1
    if p.exists() and p.is_dir():
        files = [Path(f) for f in p.iterdir()]
        if len(files) == 0:
            print("Empty directory, signing off...")
            sys.exit(1)
        else:
            report_names = [f for f in files if ('GoogleEarningsReport' in f.stem and f.suffix == '.csv')]
            if len(report_names) > 0:
                for f in report_names:
                    filename_ok = check_file_name(f.stem, type)
            else:
                print('No Google report!')
                sys.exit(1)
    else:
        print('The source dir is not dir, signing off...')
        sys.exit(1)
    return filename_ok, files


if __name__ == '__main__':
    g_checker(Path.cwd())
