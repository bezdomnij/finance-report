import smbclient
from urllib import request
import urllib
from smb.SMBHandler import SMBHandler

def main():
    opener = urllib.request.build_opener(SMBHandler)
    fh = opener.open('smb://frank:999@192.168.2.10/raiddisk/pd/ertekesito_darab_error.txt')
    data = fh.read()
    print(data)
    fh.close()


if __name__ == '__main__':
    main()