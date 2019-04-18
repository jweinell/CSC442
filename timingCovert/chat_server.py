#!/usr/bin/python


import socket
import time

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 1337
s.bind(("",port))

s.listen(0)

c, addr = s.accept()

while True:
    msg = "mystring EOF"
    for i in msg:
        c.send(i)
        print i
        time.sleep(1.0)
