#!/usr/bin/env python3

import socket
import time
# import pyglet
import Code.client_side.client_networking as netw

networking = netw.connection()

time.sleep(1)
networking.send_message(msg='siin')
time.sleep(1)
networking.send_message(msg='on')
time.sleep(1)
networking.send_message(msg='hea')
while True:
    print(networking.get_messages())
    time.sleep(1)
