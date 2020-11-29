import pyglet
from random import randint
from pyglet import shapes

def otherPlayers(numOtherPlayers):
    otherPlayers = []
    for i in range(numOtherPlayers):
        others_x = randint(0, 800)
        others_y = randint(0, 600)
        newOtherPlayers = shapes.Circle(others_x, others_y,40,color = (randint(0,255),randint(0,255),randint(0,255)))
        otherPlayers(newOtherPlayers)
    return otherPlayers
otherPlayersList = otherPlayers(4)