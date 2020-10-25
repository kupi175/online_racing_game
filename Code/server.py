#!/usr/bin/env python3

import sys
import threading
from Code.player import player as player

# host and port
host = ''
port = 12345

global available_player_pool
available_player_pool = set()
'''
Todo: create a game creator that uses the pop method to remove players from the set and move them to the 
'''

def player_creator(host, port):  # handle new players
    import socket  # import socket to be used by this function

    sys.stdout.flush()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # try to bind a socket
        socket.bind((host, port))
    except Exception as e:
        # print out error without crashing
        print(e)

    # listen to bound socket
    try:
        socket.listen()
        print('Server waiting for connections')
    except Exception as e:
        # print out error without crashing
        print(e)

    # while loop for accepting new player connections
    global available_player_pool
    while True:
        conn, address = socket.accept()
        try:
            player_object = player(conn, address)
            available_player_pool.add(player_object)
            print('Connected to:', address)
        except Exception as e:
            print(e)


        # create a new process for the connection and run it.


# ensure only main has access to code beyond this
if __name__ == '__main__':
    # initialise network connection handler
    nch = threading.Thread(target=player_creator, args=(host, port), daemon=True)
    nch.start()
    while True:
        pass
