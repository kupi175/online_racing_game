#!/usr/bin/env python3

import threading
import sys
import time

# host and port
host = ''
port = 12345



def multip_client(connection, address):
    timestamp = time.time() + 0.01
    while True:
        try:
            if 0 > (timestamp - time.time()):
                connection.send(str.encode('tst'))
                timestamp += 0.01
        except Exception as e:
            print('player', address, 'disconnected: ', e)
            break


def player_handler(host, port):  # handle new players
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
        thread = threading.Thread(target=multip_client, args=(conn, address))
        thread.start()


# ensure only main has access to code beyond this
if __name__ == '__main__':
    # initialise network connection handler
    nch = threading.Thread(target=player_handler, args=(host, port), daemon = True)
    nch.start()
    while True:
        pass
