# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib
from sys import argv
from urllib import request
from smb.SMBHandler import SMBHandler
from google_audio import rw_ga


def discover(to_find):
    print(type(to_find))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(u'smb://frank:999@192.168.2.44/raiddisk/PD/datum_darab_error.txt', )

    # Process fh like a file-like object and then close it.
    with fh as f:
        for line in f:
            print(line.decode('utf-8').strip().split('|'))
    fh.close()

    # For paths/files with unicode characters, simply pass in the URL as an unicode string
    # fh2 = director.open(u'smb://myuserID:mypassword@192.168.1.1/sharedfolder/测试文件夹/垃圾文件.dat')

    # Process fh2 like a file-like object and then close it.
    # fh2.close()


# Press the green button in the gutter to run the script.
def report():
    rw_ga.google_audio('stg_fin2_20012_google_audio', '19')


if __name__ == '__main__':
    # print_hi('PyCharm')
    if len(argv) == 1:
        print("Nincs mire nézni!")
    else:
        print(argv)
        discover(argv[1:])
        # print_hi('PyCharm')
    report()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
