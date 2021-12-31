# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib
from sys import argv
from urllib import request

from smb.SMBHandler import SMBHandler

from google_all import google_audio
from libreka import libreka


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
    google_audio.google_audio('stg_fin2_20012_google_audio', hova)
    # google.google('stg_fin2_12_googleplay', hova)


if __name__ == '__main__':
    if len(argv) == 1:
        print("Nincs mire nézni!")
    else:
        print(argv)
        discover(argv[1:])
    report('19')
    libreka.main('/Users/frank/pd/sales_report/16_libreka')
    # libreka.main('k:/PD/data/sales_report/16_libreka')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
