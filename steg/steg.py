#!/usr/bin/python
#
# Work for this project can be pulled from github with:
#
#   git clone git@github.com:jweinell/CSC442.git
#
# Related work is in the steg directory
#

import re
import sys


#Define default values for parameters
OFFSET=1024
INTERVAL=8
SENTINEL=[0,255,0,0,255,0]
store = False
retrieve = False


#Parse arguments with regular expressions
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

#Retrieve stegged data with the bit method
#
#Output take IO object
#Ending takes int list denoting two digit hex values
#Offset takes integer byte count
def bitMethod(data,offset,output,ending):
    #Initialize variables
    secret = ''
    sentinel = ''
    i = offset
    length = len(data)

    #Create sentinel string
    for value in ending:
        sentinel += chr(value)

    #Process bytes in input file
    while i < length:
        #Track bit position of hidden data
        position = (i - offset)%8

        #Reset byte value after 8 bits
        if position == 0:
            byte = 0

        #Bitwise shift byte data to add new bit
        byte = (byte<<1) + ord(data[i])%2

        #Append character to secret after 8 bit
        #Disregard initial bit
        if position == 7 and i != OFFSET:
            secret += chr(byte)
        i += 1

        #Check ending of secret for sentinel value
        #If sentinel detected set i to length to end while loop
        try:
            if secret[-1 * len(sentinel):] == sentinel:
                secret = secret[:-1 * len(sentinel)]
                i = length
        except:
            pass

    #Write secret to output
    output.write(secret)


#Retrieve stegged data with byte method
#
#Output is IO object
#Output and Interval represent byte counts
#Ending takes int list denoting two digit hex values
def byteMethod(data, offset, output, ending, interval):
    #Initialize variables
    secret = ''
    length = len(data)
    i = offset
    sentinel = ''

    #Create sentinel string
    for value in ending:
        sentinel += chr(value)

    #Process bytes in input file
    while i < length:
        secret += data[i]
        i += interval

        #Check secret for sentinel value
        try:
            if secret[-1 * len(sentinel):] == sentinel:
                secret = secret[:-1 * len(sentinel)]
                i = length
        except:
            pass

    #Write secret to output
    output.write(secret)


#Bit method to store steg data
def bitStore(data,offset,output,ending,hidden):
    #Check that hidden data will fit in wrapper
    if (len(data) - offset) <  (8 * (len(hidden) + len(ending))):
        return None

    #Append sentinel value to hidden data
    for value in ending:
        hidden += chr(value)

    #Initialize variables
    i = offset
    datalist = []

    #Convert wrapper data to list
    for character in data:
        datalist.append(character)

    #Process bytes in hidden data
    for character in hidden:
        position = 7
        charnum = ord(character)

        #Process bits in hidden data bytes
        while position >= 0:
            bit = (charnum>>position)%2
            datanum = ord(datalist[i])
            if datanum%2 == bit:
                pass
            else:
                if datanum%2 == 0:
                    datalist[i] = chr(datanum + 1)
                elif datanum%2 == 1:
                    datalist[i] = chr(datanum - 1)
            i += 1
            position -= 1

    data = ''.join(datalist)
    output.write(data)

def byteStore(data, offset, output, ending, interval, hidden):
    #Check that hidden data will fit in wrapper
    if (len(data) - offset) < (interval * (len(hidden) + len(ending))):
        return None

    #Append sentinel value to hidden data
    for value in ending:
        hidden += chr(value)

    #Initialize variables
    i = offset
    datalist = []

    #Convert data to list
    for character in data:
        datalist.append(character)

    #Overwrite data values with hidden Values
    for character in hidden:
        datalist[i] = character
        i += interval

    data = ''.join(datalist)
    output.write(data)


#Process arguments to desired method
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
