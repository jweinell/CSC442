#!/usr/bin/python
# Macedonians -- Group 1 

import socket
import sys
import time
import re
conn = ('jeangourd.com',31337) # server and port to connect to
times = []
LOWER = 0
HIGHER = 0.1 # upper delay
ASCII_TYPE = 8 # ASCII type, valid for 7 or 8

# communicate with the server, print the overt message and record the delays
def getTimes(connection):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connection)
    data = s.recv(4096)
    sys.stdout.write(data)
    # time before receiving bit
    t0 = time.time()
    sequence = []
    if len(data) > 1:
        sequence.append([None] * (len(data) - 1))
    while (data.rstrip('\n')!= 'EOF'):
        data = s.recv(4096)
        if (data.rstrip('\n') == 'EOF'):
        	break
        # time AFTER receiving bit
        t1 = time.time()
        # calculate the distances
        # then make our starting point the end of the previous
        dif = t1-t0
        t0 = t1
        sequence.append(dif)
        sys.stdout.write(data)
        sys.stdout.flush()
    s.close()
    return sequence

# Translates the timing delays into a binary string
def getCovert(timearr, lower, higher):
	binary = ""
	# compares each delay and assigns it to the closer threshold's value (0/1)
	for time in timearr:
		diflower = abs(time - lower)
		difhigher = abs(time - higher)
		# print str(diflower) + ", " + str(difhigher)
		if (diflower < difhigher):
			binary = binary + "0"
		else:
			binary = binary + "1"
	return binary

# ASCII Decoder, from previous coding assignment
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


### MAIN CODE ###
times = getTimes(conn) # translates the times from the overt messages into an array
binstr = getCovert(times, LOWER, HIGHER) # translates the delays into output
decoded = decode_ascii(binstr,ASCII_TYPE) # decodes the binary into ASCII

# attempts to take the output and strip the EOF
try:
	covert = re.compile(r'(.*)EOF')
	print covert.search(decoded).group(1)
# if this were to fail for some reason, we just print out the entire output
except AttributeError:
	print decoded
