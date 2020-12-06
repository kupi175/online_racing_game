#!/usr/bin/env python3

import sys
import threading
from Code.server_side.server_networking import player as player

# host and port
host = ''
port = 12345

general_player_pool = set()
queued_player_pool = set()
'''
Todo: create a game creators
 random matchmaking: start with random map settings. create a player pool to take players out of when the critical mass has been reached after a race players are deposited back into the player pool
 custom match: host player creates game, picks settings: seed (random, predefined), lapped or non lapped, if lapped then how many laps, possible ability to manipulate the speed of the players.
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
    global general_player_pool
    while True:
        conn, address = socket.accept()
        try:
            player_object = player(conn, address)
            general_player_pool.add(player_object)
            print('Connected to:', address)
        except Exception as e:
            print(e)


# ensure only main has access to code beyond this
if __name__ == '__main__':
    # initialise network connection handler
    nch = threading.Thread(target=player_creator, args=(host, port), daemon=True)
    nch.start()
    while True:
        pass
