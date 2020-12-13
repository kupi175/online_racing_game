'''                                             y            x,y
pygame test                                     ^
x-laius ja y-kõrgus, 0,0 on all vasakul       kõrgus
2020 Tartu Ülikool                              ^
Peeter Virk                                    0.0--laius--> x
Walther Kraam
'''

import pyglet
from pyglet.window import key, FPSDisplay
from pyglet import shapes
from random import randint
import time
import map_generator as mg

# import UI

playersFail = open('players.txt').read().split('\n')  # loeb playerite asukohad
players = []
for i in playersFail:
    i = i.split(',')
    players.append(i)
playersLen = len(players)
velx = 0
vely = 0
ymod = 3
xmod = 0.5
playerRadius = 40
ver = 'alpha 0.003'

window = pyglet.window.Window(width=1200, height=500, caption='test game', resizable=False, vsync=False)

batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()

fps_display = FPSDisplay(window)
fps_display.label.font_size = 20

player = shapes.Circle(x=int(window.width // 2), y=10, radius=playerRadius, color=(55, 55, 255), batch=batch)


def collidables(rect):  # this checks if the side wall is within the checkable area of the player
    global player
    collidableBoxes = []
    for row in rect[::2]:  # this checks with the leftmost box of the row
        if player.y-player.radius < row.y+row.height//2 < player.y+player.radius*3:
            print(row.y)
            collidableBoxes.append(row)  # the left box of the row
            collidableBoxes.append(rect[rect.index(row)+1])  # the right box of the row
    return collidableBoxes



def genMap():
    global rect, player
    seed = int(time.time() // randint(1, 1000))
    kaart = mg.game_map(seed, 100)
    kaardiAtribuudid = kaart.get_map(start=0, end=30)
    dst, ofs = kaardiAtribuudid
    laiuseKordaja = 400
    blokiKõrgus = 30
    #print(dst, ofs)
    #print(len(dst))
    rect = []
    cnt = 0

    for i in range(len(dst)):
        offset = ofs[cnt] * laiuseKordaja * 2
        if offset < 250:
            offset = 250
        distance = dst[cnt] * laiuseKordaja + window.width // 2 - (window.width // 4 + 100)
        rect.append(shapes.Rectangle(x=0, y=cnt * blokiKõrgus, width=distance, height=blokiKõrgus, color=(77, 161, 82),
                                     batch=batch2))
        rect.append(shapes.Rectangle(x=distance + offset, y=cnt * blokiKõrgus, width=window.width - (distance + offset),
                                     height=blokiKõrgus, color=(77, 161, 82), batch=batch2))
        cnt += 1
    #print(rect)
    print(len(rect))


label = pyglet.text.Label('Py test game', font_size=26, x=window.width // 2, y=window.height // 2 + 300,
                          anchor_x='center', anchor_y='center', batch=batch)
verLabel = pyglet.text.Label(str(ver), font_size=8, x=0, y=0, batch=batch)


def otherPlayers(numOtherPlayers):
    global playerRadius
    otherPlayers = []
    for i in range(numOtherPlayers):
        others_radius = playerRadius
        others_x = randint(0, window.width - others_radius)
        others_y = randint(0, window.height - others_radius)
        newOtherPlayers = shapes.Circle(x=others_x, y=others_y, radius=others_radius,
                                        color=(randint(25, 255), randint(25, 255), randint(25, 255)), batch=batch)
        otherPlayers.append(newOtherPlayers)
    return otherPlayers


otherPlayersList = otherPlayers(2)


def collisionCheck(rect):  # vaatab, kas player on collisionis hetkel seinaga, mille nimi on rect

    side = {
        'right': False,
        'left': False,
        'down': False,
    }

    for box in rect:
        if player.y + player.radius > box.y and player.y - player.radius < box.y + box.height:  # collision detection parem-vasak
            if box.x - 2 < player.x + player.radius < box.x + 10:
                # print('left')
                side['left'] = True
            else:
                side['left'] = False
            if box.x + box.width - 10 < player.x - player.radius < box.x + box.width + 2:
                # print('right')
                side['right'] = True
            else:
                side['right'] = False

        if box.x - 2 < player.x + player.radius and player.x - player.radius < box.x + box.width + 2:  # alumine col.detect
            if box.y - 2 < player.y + player.radius < box.y:
                # print('down')
                side['down'] = True
            else:
                side['down'] = False
    return side
    # print(colSide)
    # if rect.x < player.x+player.radius and player.x-player.radius < rect.x+rect.width:
    #    if rect.y <= player.y+player.radius and player.y-player.radius <= rect.y+rect.height:
    #        velx = 0


def update(velx, vely, colSide):  # tuleb implemeteerida colSide lybrariga collision side ja sellega seoses olev liikumise kiirus
    player.x += velx
    if colSide['right'] == True or colSide['left'] == True:
        print(colSide)
        player.y += 0.1
    if colSide['down'] == True:
        player.y += 0

    else:
        player.y += vely
    if player.y - player.radius >= window.height:
        genMap()  # ------------kui player liigub ekraani ülemisse serva, tehakse uus map-------------------
        player.y = 0 - player.radius
    if player.x >= window.width:
        player.x = 1
    if player.x < 0:
        player.x = window.width - 1


def draw_everything(dt):
    window.clear()
    batch.draw()
    batch2.draw()
    colRect = collidables(rect)  # who is collidable
    colSide = collisionCheck(colRect)  # checks the collision side
    update(velx, vely, colSide)  # updates the player movement and the scene
    fps_display.draw()


@window.event
def on_draw():
    draw_everything(None)


@window.event
def on_key_press(symbol, modifiers):
    global velx
    global vely
    global xmod
    global ymod
    if symbol == key.LEFT:
        if modifiers & key.MOD_CTRL:
            velx -= xmod // 2
        elif modifiers & key.MOD_SHIFT:
            velx -= xmod * 2
        else:
            velx -= xmod
    if symbol == key.RIGHT:
        if modifiers & key.MOD_CTRL:
            velx += xmod // 2
        elif modifiers & key.MOD_SHIFT:
            velx += xmod * 2
        else:
            velx += xmod
    if symbol == key.UP:
        if modifiers & key.MOD_CTRL:
            pass
            # vely += ymod / 2-ei tööta kuna key release on -ymod
        elif modifiers & key.MOD_SHIFT:
            vely += ymod * 2
        else:
            vely += ymod


@window.event
def on_key_release(symbol, modifiers):
    global velx
    global vely
    if symbol == key.LEFT:
        velx = 0

    if symbol == key.RIGHT:
        velx = 0

    if symbol == key.UP:
        vely -= ymod


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

pyglet.clock.schedule_interval(draw_everything, 1 / 120)

print(__name__)
if __name__ == 'pyglet_game_test':
    genMap()
    pyglet.app.run()
elif __name__ == '__main__':
    genMap()
    pyglet.app.run()
    # import UI
