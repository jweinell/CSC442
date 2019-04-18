#!/usr/bin/python

import socket
import sys
import time
conn = ('jeangourd.com',31337)

def getTimes(connection):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connection)
    data = s.recv(4096)
    print data
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
        if len(data) > 1:
            sequence.append([None] * (len(data)))
        else:
            sequence.append(dif)
        sys.stdout.write(data + '     ,' + str(dif) + '\n')
        sys.stdout.flush()
    s.close()
    print sequence

getTimes(conn)
