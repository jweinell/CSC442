#!/usr/bin/python

from ftplib import FTP
from StringIO import StringIO
import sys
import re

#define method
METHOD = 7

#define source variables
host = '127.0.0.1'
path = '/'
username = ''
password = ''
source = (host,path,username,password)

def fetchBinaryStr(source, method):
    (host, path, username, password) = source

    #change std out and save original
    original_stdout = sys.stdout
    unused = StringIO()
    sys.stdout = unused

    #login and set path on ftp server
    ftp = FTP(host)
    ftp.login(username,password)
    ftp.cwd(path)

    #change output to store in files string
    files_str = StringIO()
    sys.stdout = files_str
    ftp.dir()
    sys.stdout = unused

    #split output string
    files = files_str.getvalue().split('\n')

    #Parse permission segment out of files list
    permissions = re.compile(r'([a-z\-]+)')
    binary_list = []
    for file in files:
        permission_array = []
        try:
            permission_match = permissions.search(file).group(0)
        except AttributeError as e:
            permission_match = ''
        for character in permission_match:
            if character == '-':
                permission_array.append('0')
            else:
                permission_array.append('1')
        permission_binary = "".join(permission_array)
        binary_list.append(permission_binary)

    binary_str = "".join(binary_list)

    #Set stdout back to oringal
    sys.stdout = original_stdout

    return binary_str


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


print decode_ascii(fetchBinaryStr(source,METHOD),7)
