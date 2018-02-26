#!/usr/bin/python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost",10405))
data = s.recv(1024)
print("DATA: ",data)
s.close()
