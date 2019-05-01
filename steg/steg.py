#!/usr/bin/python

import re
import sys

OFFSET=1024
INTERVAL=8
SENTINEL=[0,255,0,0,255,0]

args = sys.argv

filename = 'stegged-byte.bmp'
fh = open(filename, 'rb')
content = fh.read()

def bitMethod(data,offset,output,ending):
    secret = ''
    length = len(data)

    i = offset

    while i < length:
        position = (i - offset)%8
        if position == 0:
            byte = 0
        byte = (byte<<1) + ord(data[i])%2
        #print byte
        #print position
        if position == 7 and i != OFFSET:
            secret += chr(byte)
            #print byte
        i += 1
        #print i
    for value in ending:
        secret += chr(value)
    output.write(secret)

def byteMethod(data, offset, output, ending, interval):
    secret = ''
    length = len(data)

    i = offset

    while i < length:
        secret += data[i]
        i += interval

    for value in ending:
        secret += chr(value)
    output.write(secret)

fho = open('output.jpg','wb')

#bitMethod(content, OFFSET, fho, SENTINEL)

byteMethod(content, OFFSET, fho, SENTINEL, INTERVAL)
fho.close()

fhi = open('output.jpg','rb')

content = fhi.read()
fho2 = open('output2.txt','wb')

byteMethod(content, 1025, fho2, SENTINEL, 5)

#print decode_ascii(secret,8)

#print binascii.unhexlify(binascii.hexlify(content))

#print len(content)
