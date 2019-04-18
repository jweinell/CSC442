#!/usr/bin/python

import socket
import sys
import time
import re
conn = ('jeangourd.com',31337)
times = []
LOWER = 0
HIGHER = 0.1
ASCII_TYPE = 8

def getTimes(connection):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connection)
    data = s.recv(4096)
    sys.stdout.write(data)
    t0 = time.time()
    sequence = []
    if len(data) > 1:
        sequence.append([None] * (len(data) - 1))
    while (data.rstrip('\n')!= 'EOF'):
        data = s.recv(4096)
        if (data.rstrip('\n') == 'EOF'):
        	break
        t1 = time.time()
        #print(t1 - t0)
        dif = t1-t0
        t0 = t1
        sequence.append(dif)
        sys.stdout.write(data)
        sys.stdout.flush()
    s.close()
    return sequence

def getCovert(timearr, lower, higher):
	binary = ""
	for time in timearr:
		diflower = abs(time - lower)
		difhigher = abs(time - higher)
		# print str(diflower) + ", " + str(difhigher)
		if (diflower < difhigher):
			binary = binary + "0"
		else:
			binary = binary + "1"
	return binary

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

times = getTimes(conn)
binstr = getCovert(times, LOWER, HIGHER)
# print binstr
decoded = decode_ascii(binstr,ASCII_TYPE)

try:
	covert = re.compile(r'(.*)EOF')
	print covert.search(decoded).group(1)
except AttributeError:
	print decoded
