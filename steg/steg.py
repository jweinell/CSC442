#!/usr/bin/python

import re
import sys

OFFSET=1024
INTERVAL=8
SENTINEL=[0,255,0,0,255,0]

store = False
retrieve = False

args = sys.argv

for argument in args:
    if re.match(r'^-b',argument):
        method = 'bit'
    elif re.match(r'^-B',argument):
        method = 'byte'
    elif re.match(r'^-s',argument):
        store = True
    elif re.match(r'^-r',argument):
        retrieve = True
    elif re.match(r'^-o([0-9]*)',argument):
        OFFSET = re.search(r'-o([0-9]*)',argument).group(1)
    elif re.match(r'^-i([0-9]*)',argument):
        INTERVAL = re.search(r'-i([0-9]*)',argument).group(1)
    elif re.match(r'^-w(.*)',argument):
        wrapper = re.search(r'-w(.*)',argument).group(1)
    elif re.match(r'^-h(.*)',argument):
        hidden = re.search(r'-h(.*)',argument).group(1)

filename = 'stegged-byte.bmp'
fh = open(filename, 'rb')
content = fh.read()

def bitMethod(data,offset,output,ending):
    secret = ''
    length = len(data)
    i = offset
    sentinel = ''
    for value in ending:
        sentinel += chr(value)
    while i < length:
        position = (i - offset)%8
        if position == 0:
            byte = 0
        byte = (byte<<1) + ord(data[i])%2
        if position == 7 and i != OFFSET:
            secret += chr(byte)
        i += 1
        try:
            if secret[-1 * len(sentinel):] == sentinel:
                secret = secret[:-1 * len(sentinel)]
                i = length
        except:
            pass

    output.write(secret)

def byteMethod(data, offset, output, ending, interval):
    secret = ''
    length = len(data)

    i = offset
    sentinel = ''
    for value in ending:
        sentinel += chr(value)
    while i < length:
        secret += data[i]
        i += interval
        try:
            if secret[-1 * len(sentinel):] == sentinel:
                secret = secret[:-1 * len(sentinel)]
                i = length
        except:
            pass

    output.write(secret)

def bitStore(data,offset,output,ending,hidden):
    if (len(data) - offset) <  (8 * (len(hidden) + len(ending))):
        return None

    for value in ending:
        hidden += chr(value)

    i = offset

    datalist = []
    for character in data:
        datalist.append(character)

    for character in hidden:
        position = 7
        charnum = ord(character)
        while position >= 0:
            bit = (charnum>>position)%2
            datanum = ord(datalist[i])
            if datanum%2 == bit:
                pass
            else:
                if datanum%2 == 0:
                    #print datanum
                    #exit()
                    datalist[i] = chr(datanum + 1)
                elif datanum%2 == 1:
                    datalist[i] = chr(datanum - 1)
            i += 1
            position -= 1

    data = ''.join(datalist)
    output.write(data)

def byteStore(data, offset, output, ending, interval, hidden):
    if (len(data) - offset) < (interval * (len(hidden) + len(ending))):
        return None

    for value in ending:
        hidden += chr(value)

    i = offset

    datalist = []
    for character in data:
        datalist.append(character)
    for character in hidden:
        datalist[i] = character
        i += interval
    data = ''.join(datalist)
    output.write(data)





if retrieve and not store:
    if method == 'bit':
        fhr = open(wrapper,'rb')
        content = fhr.read()
        bitMethod(content,int(OFFSET),sys.stdout,SENTINEL)
        fhr.close()
    elif method == 'byte':
        fhr = open(wrapper,'rb')
        content = fhr.read()
        byteMethod(content,int(OFFSET),sys.stdout,SENTINEL,int(INTERVAL))
        fhr.close()
elif store and not retrieve:
    if method == 'bit':
        fhr = open(wrapper,'rb')
        content = fhr.read()
        fhh = open(hidden,'rb')
        hiddendata = fhh.read()
        bitStore(content,int(OFFSET),sys.stdout,SENTINEL,hiddendata)
        fhr.close()
    elif method == 'byte':
        fhr = open(wrapper,'rb')
        content = fhr.read()
        fhh = open(hidden,'rb')
        hiddendata = fhh.read()
        byteStore(content,int(OFFSET),sys.stdout,SENTINEL,int(INTERVAL),hiddendata)
        fhr.close()
else:
    pass


#fho = open('output.jpg','wb')

#bitMethod(content, OFFSET, fho, SENTINEL)

#byteMethod(content, OFFSET, fho, SENTINEL, INTERVAL)
#fho.close()

#fhi = open('output.jpg','rb')

#content = fhi.read()
#fho2 = open('output2.txt','wb')

#byteMethod(content, 1025, fho2, SENTINEL, 5)

#print decode_ascii(secret,8)

#print binascii.unhexlify(binascii.hexlify(content))

#print len(content)
