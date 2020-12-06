#!/usr/bin/env python3

import time
import pyglet
import Code.client_side.client_networking as netw

window = pyglet.window.Window(width=1200, height=900, caption='test game', resizable=False, vsync=False)
batch = pyglet.graphics.Batch()
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label.font_size = 20

networking = netw.connection('127.0.0.1')
networking.send_message(msg=str('hei'))

while True:
    print(networking.get_messages())
    time.sleep(1)








if __name__ == '__main__':
    # creating the display

    pyglet.app.run()
    #establishing a network connection
