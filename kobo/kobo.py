from pathlib import Path
from config import MAIN_DIR, REPORT_MONTH, HOVA
import util
from engineer import sql_writer as sqw
from result import Result

TABLE_1 = 'stg_fin2_2_kobo_drm'
TABLE_2 = 'stg_fin2_2_kobo_nodrm'
FILENAME = 'PublishDrive Kft_CONTENT2CONNECT'
DATA_DIR = 'kobo'
SUM_FIELD = 'Net Due (Payable Currency)'
DATE_FIELD = 'Date'


def kobo(hova=HOVA):
    res = []
    p = Path(MAIN_DIR).joinpath(REPORT_MONTH).joinpath(DATA_DIR)
    files = util.get_file_list(p)

    if files is None:
        return
    if len(files) > 0:
        for f in files:
            marker = '_NODRM'
            if f.is_file() and f.stem[:2] not in ['~$', '.D'] and 'Sub' not in f.stem and 'plus' not in f.stem:
                print(f)
                df2 = util.get_proper_df(f)  # remove spaces from field names
                # print(df2.columns)
                szumma = df2[SUM_FIELD].sum()
                record_count = df2.shape[0]
                print('!!! A frame merete', df2.shape[0])
                print(f.stem)
                date_borders = util.get_df_dates(DATE_FIELD, 3, df2)
                if '_DRM' in f.stem.upper():
                    marker = '_DRM'
                    sqw.write_to_db(df2, TABLE_1, hova=hova, field_lens='vchall')
                    res.append(Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                      'USD', 'drm', szumma, date_borders[0], date_borders[1]))
                else:
                    sqw.write_to_db(df2, TABLE_2, hova=hova, field_lens='vchall')
                    res.append((Result(DATA_DIR.upper(), REPORT_MONTH, record_count,
                                       'USD', 'nodrm', szumma, date_borders[0], date_borders[1])))
                print(f"{(DATA_DIR + marker).upper()}, "
                      f"{REPORT_MONTH}, {record_count} records, total: {szumma:-12,.3f}\n")
    else:
        util.empty(DATA_DIR)
    return res


def main():
    kobo(hova='0')


if __name__ == '__main__':
    main()
