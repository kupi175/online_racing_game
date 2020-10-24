#!/usr/bin/env python3

import socket
# import pyckle
import multiprocessing
import sys
import time

min_version = 0.01

# host and port
host = ''
port = 12345

processes = []

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def multip_client(connection, pid):
    sys.stdout.flush()
    conn.recv(2048)
    timestamp = time.time() + 0.01
    while True:
        try:
            if 0 > (timestamp - time.time()):
                connection.send(str.encode('tst'))
                timestamp += 0.01
        except Exception as e:
            print(e)
            break


# ensure only main has access to code beyond this
if __name__ == '__main__':
    try:
        # try to bind a socket
        socket.bind((host, port))
    except Exception as e:
        # print out error without crashing
        print(e)

    # listen to binded socket
    try:
        socket.listen()
        print('Server started, waiting for connection')
    except Exception as e:
        # print out error without crashing
        print(e)
    # while loop for accepting new player connections
    c_pid = 0
    while True:
        conn, addr = socket.accept()
        print('Connected to:', addr)

        # create a new process for the connection and run it.
        process = multiprocessing.Process(target=multip_client, args=(conn, c_pid))
        process.start()
        c_pid += 1
