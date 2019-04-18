#!/usr/bin/python

import socket
import sys
import time
conn = ('jeangourd.com',31337)
times = []
LOWER = 0
HIGHER = 1

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
		diflower = abs(timearr[time] - lower)
		difhigher = abs(timearr[time] - higher)
		if (diflower < difhigher):
			binary = binary + "0"
		else:
			binary = binary + "1"
	return binary

times = getTimes(conn)

