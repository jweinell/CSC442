#!/usr/bin/python

from random import randint

def toBinary(text, bits=7):
    binArray = []
    for character in text:
        nonstandard = bin(ord(character))[2:]
        binArray.append('0' * (bits - len(nonstandard)) + nonstandard)
    return "".join(binArray)

def intBinary(integer, length = 0):
    max = 2 ** length
    binstr = bin(integer)[2:]
    binstr = '0' * (length - len(binstr)) + binstr
    return binstr

def getPermissions(bindata,method):
    bindata = bindata + ('0' * (method - len(bindata)%method))
    chunks = [bindata[i:i+method] for i in range(0, len(bindata), method)]
    i = 0
    while i < len(chunks):
        chunks[i] = ('0' * (10 - method)) + chunks[i]
        i = i + 1
    return chunks

def saltFiles(permissions, method):
    front = 10 - method
    back = method
    newPermissions = []
    i = 0
    while i < len(permissions):
        r = randint(1,5)
        if r == 1:
            saltPerm = intBinary(randint(1,2**front - 1), front)
            saltPerm = saltPerm + intBinary(randint(1,2**back - 1), back)
            newPermissions.append(saltPerm)
        else:
            newPermissions.append(permissions[i])
            i = i + 1
    return newPermissions

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

def encodeCovert():
    pass

#print intBinary(6,5)
method = 5
permissions = getPermissions(toBinary('text'), method)
saltPermissions = saltFiles(permissions, method)
print permissions
print saltPermissions

#print toBinary('sometext', bits = 8)
