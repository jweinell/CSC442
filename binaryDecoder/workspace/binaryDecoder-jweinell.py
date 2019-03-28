#!/usr/bin/python

import sys

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


bindata = sys.stdin.readline().strip()

decoded8 =  decode_ascii(bindata,8)
decoded7 = decode_ascii(bindata,7)
if decoded7:
    print "7-bit ascii:\n" + decoded7
if decoded8:
    print "8-bit ascii:\n" + decoded8
