#!/usr/bin/env python3

import socket
# import multiprocessing
# import pyglet
import time

#info about the default ip and port
version = '0.01'
host = '139.162.136.115'
port = 12345

#create the socket and form address
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = (host, port)

#try to connect to ip:port
try:
    socket.connect(addr)
except Exception as e:
    print(e)

timestamp = time.time()
while True:
    print(socket.recv(1024 * 2).decode('utf-8'))
    print(1 / (time.time() - timestamp))
    timestamp = time.time()
