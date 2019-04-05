#!/usr/bin/python

from ftplib import FTP
from StringIO import StringIO
import sys
import re

#Try and pull path as an argument
try:
    path = sys.argv[1]
except:
    path = '/'

#define source variables
host = '127.0.0.1'
username = ''
password = ''
source = (host,path,username,password)




#Method for retrieving a binary string from file permissions
#in a given directory on an fto serverself.
#Source parameter is a tuple with host, path, username, and password
#Method represents the number of bits of the permissions to be used
def fetchBinaryStr(source, method, hidden=False, filter=False):
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
    if hidden:
        ftp.retrlines('LIST -a')
    else:
        ftp.retrlines('LIST')

    #Set stdout back to oringal
    sys.stdout = original_stdout

    #split output string
    files = files_str.getvalue().split('\n')

    #Remove . and .. for hidden
    if hidden:
        files = files[2:]

    #Filter files
    if filter:
        pass

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

    #remove any items that have non-zero preceeding bits
    binary_list_corrected = []
    for binstr in binary_list:
        beginning = binstr[:-1 * method]
        end = binstr[-1 * method:]
        if '1' not in beginning:
            binary_list_corrected.append(end)
        else:
            pass

    #Combine list into single binary string
    binary_str = "".join(binary_list_corrected)

    return binary_str

#Used for decoding binary strings
#Takes a binary string and integer representing encoding as params
def decode_ascii(binstr, bits):
    modification = bits - len(binstr)%bits
    index = 0
    mod_list = []
    while index < modification:
        binstr = binstr + '0'
        index = index + 1
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

def challengeMethod(source):
    methods = [10,8,7]
    for method in methods:
        methodStr = 'Method ' + str(method) + ':\n'
        print methodStr
        print '  7-bit:   ' + decode_ascii(fetchBinaryStr(source, method),7)
        print '  8-bit:   ' + decode_ascii(fetchBinaryStr(source, method),8)
        print '  7-bitH:  ' + decode_ascii(fetchBinaryStr(source, method, hidden=True),7)
        print '  8-bitH:  ' + decode_ascii(fetchBinaryStr(source, method, hidden=True),8)
        print ''

challengeMethod(source)

#Fetch the binary string and normalize it for decoding
#binary_str = normalizeBinary(fetchBinaryStr(source,METHOD),7)

#print decode_ascii(binary_str,7)
