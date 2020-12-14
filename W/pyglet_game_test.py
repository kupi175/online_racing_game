'''                                             y            x,y
pygame test                                     ^
x-laius ja y-kõrgus, 0,0 on all vasakul       kõrgus
2020 Tartu Ülikool                              ^
Peeter Virk                                    0.0--laius--> x
Walther Kraam
-------
player movement
vel - is calculated through the mod variable
mod - change in velocity
arrow buttons only change the mod variable!
-------
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
velxMax = 4
velyMax = 4
ymod = 1
xmod = 0.2
playerRadius = 40
keys = []  # for keys that are held down
ver = 'beta 0.010'
window = pyglet.window.Window(width=1200, height=500, caption='test game', resizable=False, vsync=False)

batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()

fps_display = FPSDisplay(window)
fps_display.label.font_size = 20

player = shapes.Circle(x=window.width // 2, y=10, radius=playerRadius, color=(55, 55, 255), batch=batch)


def collidables(rect):  # this checks if the side wall is within the checkable area of the player
    global player
    collidableBoxes = []
    for row in rect[::2]:  # this checks with the leftmost box of the row
        if player.y - player.radius < row.y + row.height // 2 < player.y + player.radius * 3:
            # print(row.y)
            collidableBoxes.append(row)  # the left box of the row
            collidableBoxes.append(rect[rect.index(row) + 1])  # the right box of the row
    return collidableBoxes


def genMap():
    global rect, player
    seed = int(time.time() // randint(1, 1000))
    kaart = mg.game_map(seed, 100)
    kaardiAtribuudid = kaart.get_map(start=0, end=30)
    dst, ofs = kaardiAtribuudid
    laiuseKordaja = 400
    blokiKõrgus = 30
    # print(dst, ofs)
    # print(len(dst))
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
    # print(rect)
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
    playerNextPosY = player.y + vely  # kus on player enda järgmise ticki ajal y-suunal
    playerNextPosX = player.x + velx  # kus on player enda järgmise ticki ajal x-suunal

    for box in rect:
        if box.y < playerNextPosY + player.radius and playerNextPosY - player.radius < box.y + box.height:  # collision detection parem-vasak
            if box.x - 2 <= playerNextPosX + player.radius <= box.x + 2:
                print('left')
                side['left'] = True
            else:
                side['left'] = False
            if box.x + box.width - 2 <= playerNextPosX - player.radius <= box.x + box.width + 2:
                print('right')
                side['right'] = True
            else:
                side['right'] = False

        if box.x - 2 < playerNextPosX + player.radius and playerNextPosX - player.radius < box.x + box.width + 2:  # alumine col.detect
            if box.y - 2 < playerNextPosY + player.radius < box.y:
                # print('down')
                side['down'] = True
            else:
                side['down'] = False
        if True in side.values():
            return side
    return side
    # print(colSide)
    # if rect.x < player.x+player.radius and player.x-player.radius < rect.x+rect.width:
    #    if rect.y <= player.y+player.radius and player.y-player.radius <= rect.y+rect.height:
    #        velx = 0


def update(colSide):  # tuleb implemeteerida colSide lybrariga collision side ja sellega seoses olev liikumise kiirus
    global velx, vely, ymod, xmod
    #print(keys) #  for debug
    #horisontaalne liikumine <----->
    if 'd' in keys:
        if velx <= velxMax:
            velx += xmod
    elif 'a' not in keys:
        velx -= xmod
        if velx < 0.5:
            velx = 0

    if 'a' in keys:
        if velx >= -velxMax:
            velx -= xmod
    elif 'd' not in keys:
        velx += xmod
        if velx > -0.5:
            velx = 0
    #vertikaalne liikumine ^\v
    if 'w' in keys:
        if vely <= velyMax:
            vely += ymod
            if vely > velyMax:
                vely = velyMax
    else:
        if vely > 0.01:
            vely -= 0.1
    if 's' in keys:
        if vely > 0:
            vely -= 0.01
            if vely < 0.02:
                vely = 0



    # kui on collision seinaga, siis ta vertikaalne(y) kiirus on 0.1 ja horisontaalne(x) kiirus 0
    # ning ei saa liikuda sinna suunas, kus on sein ees.
    '''if colSide['right'] == True or colSide['left'] == True:
        xmod = 0
        ymod = 0
        vely = 0.1

        if colSide['right'] == True and 'a' in keys:
            xmod = 0
        if colSide['left'] == True and 'd' in keys:
            xmod = 0'''

    #playeri uue asukoha välja arvutamine
    player.x += velx
    player.y += vely

    # playeri asukoht siis kui ta on ekraani piirides, peaks ta sinna juhtuma
    if player.y - player.radius >= window.height:
        genMap()  # ------------kui player liigub ekraani ülemisse serva, tehakse uus map-------------------
        player.y = 0 - player.radius
    if player.x >= window.width:
        player.x = 1
    if player.x < 0:
        player.x = window.width - 1


def draw_everything(dt):
    global keys
    window.clear()
    batch.draw()
    batch2.draw()
    colRect = collidables(rect)  # who is collidable
    colSide = collisionCheck(colRect)  # checks the collision side
    update(colSide)  # updates the player movement and the scene
    fps_display.draw()

@window.event
def on_draw():
    draw_everything(None)


@window.event
def on_key_press(symbol, modyfiers):
    if symbol == key.LEFT or symbol == key.A:
        keys.append('a')
    if symbol == key.RIGHT or symbol == key.D:
        keys.append('d')
    if symbol == key.UP or symbol == key.W:
        keys.append('w')
    if symbol == key.DOWN or symbol == key.S:
        keys.append('s')


@window.event
def on_key_release(symbol, modyfiers):
    if symbol == key.LEFT or symbol == key.A:
        keys.remove('a')
    if symbol == key.RIGHT or symbol == key.D:
        keys.remove('d')
    if symbol == key.UP or symbol == key.W:
        keys.remove('w')
    if symbol == key.DOWN or symbol == key.S:
        keys.remove('s')


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
