#!/usr/bin/env python3

import multiprocessing
import sys
import time

# host and port
host = ''
port = 12345


def multip_client(connection):

    timestamp = time.time() + 0.01
    while True:
        try:
            if 0 > (timestamp - time.time()):
                connection.send(str.encode('tst'))
                timestamp += 0.01
        except Exception as e:
            print(e)
            break


def network_connection_handler(host,port):
    import socket
    sys.stdout.flush()

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # try to bind a socket
        socket.bind((host, port))
    except Exception as e:
        # print out error without crashing
        print(e)

    # listen to binded socket
    try:
        socket.listen()
        print('Server waiting for connections')
    except Exception as e:
        # print out error without crashing
        print(e)

    # while loop for accepting new player connections
    while True:
        conn, address = socket.accept()
        print('Connected to:', address)

        # create a new process for the connection and run it.
        process = multiprocessing.Process(target=multip_client, args=(conn))
        process.daemon = True
        process.start()


# ensure only main has access to code beyond this
if __name__ == '__main__':
    # initialise network connection handler
    nch = multiprocessing.Process(target=network_connection_handler, args=(host,port))
    nch.start()
    while True:
        pass
