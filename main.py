# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import urllib
from sys import argv
from urllib import request

from smb.SMBHandler import SMBHandler

import kobo
import stores
from apple_finrep import apples


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
def report(hova='0'):
    # directory = '/Users/frank/pd/Nextcloud/szamitas'
    directory = 'h:/NextCloud/Finance/szamitas'

    stores.tfsymbols(hova)
    stores.amz_read(hova)
    apples.apple(hova)
    stores.bibliotheca(hova)  # DELETE table first!!!
    stores.bn(hova)
    stores.bookmate(hova)
    stores.cnpiec(hova)
    stores.dangdang(hova)
    stores.dibook(hova)
    stores.ekonyv(hova)
    stores.findaway(hova)
    stores.gardners(hova)
    stores.google(hova)
    stores.google_audio(hova)
    stores.hoopla(hova)
    stores.ireader(hova)
    kobo.kobo(hova)
    kobo.kobo_audio(hova)
    kobo.kobo_plus(hova)
    stores.libreka(hova)
    stores.mackin(hova)
    stores.odilo(hova)
    stores.perlego(hova)
    stores.scribd(hova)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    if len(argv) == 1:
        print("Nincs mire nézni!!!")
    else:
        print(argv)
        discover(argv[1:])
    # HOVA IRUNK?
    report('19')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
