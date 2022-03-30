# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import urllib
from sys import argv
from urllib import request
from smb.SMBHandler import SMBHandler

from apple_finrep import apples
import stores
import kobo


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
def report(hova='19'):
    # directory = '/Users/frank/pd/Nextcloud/szamitas'
    # directory = 'h:/NextCloud/Finance/szamitas/2021_11_november'
    directory = 'h:/NextCloud/Finance/szamitas'

    stores.tfsymbols(directory, hova)
    # stores.amz_read(directory, hova)
    apples.apple(directory, hova)
    stores.bibliotheca(directory, hova)  # DELETE table first!!!
    stores.bn(directory, hova)
    stores.bookmate(directory, hova)
    stores.cnpiec(directory, hova)
    stores.dibook(directory, hova)
    stores.ekonyv_rw(directory, hova)
    stores.findaway(directory, hova)
    stores.gardners(directory, hova=hova)
    stores.google(directory, hova)
    stores.google_audio(directory, hova)
    stores.ireader(directory, hova)
    kobo.kobo(directory, hova)
    kobo.kobo_audio(directory, hova)
    kobo.kobo_plus(directory, hova)
    stores.libreka(directory, hova)
    stores.mackin(directory, hova)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
    if len(argv) == 1:
        print("Nincs mire nézni!!!")
    else:
        print(argv)
        discover(argv[1:])
    # HOVA IRUNK?
    report('0')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
