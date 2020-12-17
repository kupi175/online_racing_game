'''run the file form here'''
import UI
import pyglet
pyglet.clock.schedule_interval(draw_everything, 1 / 90)