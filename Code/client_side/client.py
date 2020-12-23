#!/usr/bin/env python3

import time
import pyglet
import Code.duplicated.map_generator as mg
import Code.client_side.client_networking as netw

networking = netw.connection('127.0.0.1')
networking.send_message(msg=str('hei'))

while True:
    print(networking.get_messages())
    time.sleep(1)