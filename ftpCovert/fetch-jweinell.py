#!/usr/bin/python

from ftplib import FTP
import sys
import re

#define method
METHOD = 7

#define source variables
host = ''
path = '/'
username = ''
password = ''


def fetchBinaryStr(host, path, username, password, method):
    #change std out and save original
    original_stdout = sys.stdout
    unused = StringIO()
    sys.stdout = result

    #login and set path on ftp server
    ftp = FTP(host)
    ftp.login(username,password)
    ftp.cwd(path)

    #change output to store in files string
    files_str = StringIO()
    sys.stdout = files
    files = ftp.dir()
    sys.stdout = unused

    #split output string
    files = files.getvalue().split('\n')


def decode_ascii(binstr, bits):
    if len(binstr)%bits != 0:
        return None
    chrarray = []
    while len(binstr) > 0:
        chrnum = int(binstr[:bits],2)
        if chrnum != 8:
            chrarray.append(chr(chrnum))
        else:
            if len(chrarray) > 0:
                chrarray = chrarray[:-1]
        binstr = binstr[bits:]
    decoded = "".join(chrarray)
    return decoded
