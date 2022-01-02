# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import urllib
from sys import argv
from urllib import request

from smb.SMBHandler import SMBHandler

from apple_finrep import apples
from google_all import google_audio, google
from stores import amazon, bn


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
    # directory = '/Users/frank/pd/finance_report'
    directory = 'h:/NextCloud/Finance/szamitas/2021_11_november'
    google_audio.google_audio(directory, 'stg_fin2_20012_google_audio', hova)
    google.google(directory, 'stg_fin2_12_googleplay', hova)
    amazon.amz_read(directory, hova)
    bn.main(directory, hova)
    apples.main(directory, hova)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w')
    if len(argv) == 1:
        print("Nincs mire nézni!")
    else:
        print(argv)
        discover(argv[1:])
    report('19')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
