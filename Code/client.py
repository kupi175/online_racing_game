#!/usr/bin/env python3

import socket
# import multiprocessing
# import pyglet
import time

version = '0.01'
host = '176.46.100.55'
port = 12345
pid = 0

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = (host, port)

try:
    soc.connect(addr)
    soc.send(str.encode('tst'))
except:
    pass
timestamp = time.time()
while True:
    print(soc.recv(1024 * 2).decode('utf-8'))
    print(1 / (time.time() - timestamp))
    timestamp = time.time()
