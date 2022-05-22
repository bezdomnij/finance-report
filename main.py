# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import urllib
from sys import argv
from urllib import request
from config import HOVA
import pandas as pd
from smb.SMBHandler import SMBHandler
import apple_finrep
import kobo
import stores
from engineer import sql_writer as sqw


def discover(to_find):
    print(type(to_find))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    read_network()

    # For paths/files with unicode characters, simply pass in the URL as a unicode string
    # fh2 = director.open(u'smb://myuserID:mypassword@192.168.1.1/sharedfolder/测试文件夹/垃圾文件.dat')

    # Process fh2 like a file-like object and then close it.
    # fh2.close()


def read_network():
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(u'smb://frank:999@192.168.2.44/raiddisk/PD/datum_darab_error.txt', )
    # Process fh like a file-like object and then close it.
    with fh as f:
        for line in f:
            print(line.decode('utf-8').strip().split('|'))
    fh.close()


# Press the green button in the gutter to run the script.
def make_df(lst):
    df = pd.DataFrame(lst)
    # df.info()
    return df


def report():
    collect_lst = []
    # collect_lst.extend(stores.tfsymbols())
    collect_lst.extend(stores.amz_read())
    collect_lst.extend(apple_finrep.apples.apple())
    collect_lst.extend(stores.bibliotheca())  # DELETE table first!!!
    # collect_lst.extend(stores.bn())
    # collect_lst.extend(stores.bookmate())
    # collect_lst.extend(stores.bookmate_audio())
    # collect_lst.extend(stores.ciando())
    # collect_lst.extend(stores.cnpiec())
    # collect_lst.extend(stores.dangdang())
    # collect_lst.extend(stores.dibook())
    # collect_lst.extend(stores.dreame_month())
    # collect_lst.extend(stores.ekonyv())
    # collect_lst.extend(stores.eletoltes())
    # collect_lst.extend(stores.findaway())
    # collect_lst.extend(stores.gardners())
    # collect_lst.extend(stores.google())
    # collect_lst.extend(stores.google_audio())
    # collect_lst.extend(stores.hoopla())
    # collect_lst.extend(stores.ireader())
    # collect_lst.extend(kobo.kobo())
    # collect_lst.extend(kobo.kobo_audio())
    # collect_lst.extend(kobo.kobo_plus())
    # collect_lst.extend(stores.libreka())
    # collect_lst.extend(stores.mackin())
    # collect_lst.extend(stores.multimediaplaza())
    # collect_lst.extend(stores.odilo())
    # collect_lst.extend(stores.overdrive())
    # collect_lst.extend(stores.perlego())
    # collect_lst.extend(stores.scribd())
    # collect_lst.extend(stores.storytel())
    # collect_lst.extend(stores.voxa())
    # make_df(collection)
    print(collect_lst)
    df_all = pd.DataFrame(collect_lst)
    sqw.write_to_db(df_all, 'fin_results', field_lens='vchall', hova='19')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    if len(argv) == 1:
        print("Nincs mire nézni!!!\n")
    else:
        print(argv)
        discover(argv[1:])
    # HOVA IRUNK?
    DF_FINAL = pd.DataFrame()
    report()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
