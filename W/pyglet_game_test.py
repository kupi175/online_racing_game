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
milline võiks näha välja serverile saadetav info(player_x, player_y)
serverilt tulev info(kas mäng käib? 1/0 , teiste playerite x/y list[(x1,y1),(x2,y2),...,(xn,yn)])
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
ymod = 0.01
xmod = 0.2
playerRadius = 40
keys = []  # for keys that are held down
ver = 'beta 0.04' #  0.05 on siis kui networkingu tehtud saab - teised playerid tulevad nähtavale
window = pyglet.window.Window(width=1200, height=500, caption='test game', resizable=False, vsync=False)

batch = pyglet.graphics.Batch()
batchBlock = pyglet.graphics.Batch()


fps_display = FPSDisplay(window)
fps_display.label.font_size = 20

player = shapes.Circle(x=window.width // 2, y=10, radius=playerRadius, color=(55, 55, 255), batch=batch)


def genStagingarea(list,start , len, color=(255, 255, 255), blokiKõrgus = 30):
    len=start+len
    for block in range(start, len):
        list.append(shapes.Rectangle(x=0, y=block * blokiKõrgus, width=window.width//4+100, height=blokiKõrgus, color=color,
                                     batch=batchBlock))
        list.append(shapes.Rectangle(x=window.width//4+500, y=block * blokiKõrgus, width=window.width - (window.width//4+500),
                                     height=blokiKõrgus, color=color, batch=batchBlock))
    return list

def genMap():
    global rect, player
    mapLength = 200
    startFinishLength = 10
    seed = int(time.time() // randint(1, 1000))
    kaart = mg.game_map(seed, 100)
    kaardiAtribuudid = kaart.get_map(start=0, end=mapLength)
    dst, ofs = kaardiAtribuudid
    laiuseKordaja = 400
    blokiKõrgus = 30
    blockColor = (124, 230, 112)
    # print(dst, ofs)
    # print(len(dst))
    rect = []
    cnt = 0
    rect = genStagingarea(rect, 0, startFinishLength, color=(38, 255, 38))

    for i in range(startFinishLength, len(dst)):
        offset = ofs[cnt] * laiuseKordaja * 2
        if offset < 250:
            offset = 250
        distance = dst[cnt] * laiuseKordaja + window.width // 2 - (window.width // 4 + 100)
        rect.append(shapes.Rectangle(x=0, y=i * blokiKõrgus, width=distance, height=blokiKõrgus, color=blockColor,
                                     batch=batchBlock))
        rect.append(shapes.Rectangle(x=distance + offset, y=i * blokiKõrgus, width=window.width - (distance + offset),
                                     height=blokiKõrgus, color=blockColor, batch=batchBlock))
        cnt += 1

    rect = genStagingarea(rect, mapLength, startFinishLength, color=(255, 38, 38))
    # print(rect)
    print(len(rect))

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


def collidables(rect):  # this checks if the side wall is within the checkable area of the player
    global player
    collidableBoxes = []
    for row in rect[::2]:  # this checks with the leftmost box of the row
        if player.y - player.radius < row.y + row.height // 2 < player.y + player.radius * 3:
            # print(row.y)
            collidableBoxes.append(row)  # the left box of the row
            collidableBoxes.append(rect[rect.index(row) + 1])  # the right box of the row
    return collidableBoxes


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
            if box.x - 2 <= playerNextPosX + player.radius <= box.x + 200:
                side['left'] = True
            else:
                side['left'] = False
            if box.x + box.width - 200 <= playerNextPosX - player.radius <= box.x + box.width + 2:
                side['right'] = True
            else:
                side['right'] = False

        if box.x - 2 <= playerNextPosX + player.radius and playerNextPosX - player.radius <= box.x + box.width + 2:  # alumine col.detect
            if box.y - 2 < playerNextPosY + player.radius < box.y + 10:
                side['down'] = True
            else:
                side['down'] = False
        if True in side.values():
            return side
    return side


def update(colSide):  # tuleb implemeteerida colSide lybrariga collision side ja sellega seoses olev liikumise kiirus
    global velx, vely, ymod, xmod

    otherPlayersList = otherPlayers(10)

    # kui on collision seinaga, siis ta vertikaalne(y) kiirus on 0.1 ja horisontaalne(x) kiirus 0
    # ning ei saa liikuda sinna suunas, kus on sein ees.
    if colSide['left'] or colSide['right']:
        velx = 0
    if colSide['down']:
        vely = 0
        ymod = 0
        if colSide['left'] or colSide['right']:
            velx = 0
    if ymod == 0 and colSide['down'] == False:
        ymod = 0.2
    # print(keys) #  for debug

    # horisontaalne liikumine <----->
    if 'd' in keys and colSide['left'] == False:
        if velx <= velxMax:
            velx += xmod
    elif 'a' not in keys:
        velx -= xmod
        if velx < 0.3:
            velx = 0

    if 'a' in keys and colSide['right'] == False:
        if velx >= -velxMax:
            velx -= xmod
    elif 'd' not in keys:
        velx += xmod
        if velx > -0.3:
            velx = 0

    # vertikaalne liikumine ^\v
    if 'w' in keys:
        if vely <= velyMax:
            vely += ymod
            if vely > velyMax:
                vely = velyMax
    else:
        if vely > 0.01:
            vely -= 0.08
    if 's' in keys:
        if vely > 0:
            vely -= 0.01
            if vely < 0.02:
                vely = 0

    # playeri uue asukoha välja arvutamine
    player.x += velx
    '''player.y += vely'''

    # backgroundi liigutamine - et tekiks rolling effekt ja mingist momendist alumiste blockide ära lõhkumine
    for block in rect:
        block.y -= vely
        if block.y < -160:
            if len(rect) > 2:
                del rect[0]
                del rect[1]


    # teiste playerite asukohtade uuendamine
    getOthersPos(otherPlayersList)

    # playeri asukoht siis kui ta on ekraani piirides, peaks ta sinna juhtuma
    if player.y - player.radius >= window.height:
        genMap()  # ------------kui player liigub ekraani ülemisse serva, tehakse uus map-------------------
        player.y = 0 - player.radius
    if player.x >= window.width:
        player.x = 1
    if player.x < 0:
        player.x = window.width - 1


def getOthersPos(positionInfo):
    # todo: siia teha, et ta saaks teiste playerite asukoha.
    pass

def sendToServer(playerPosition):
    # todo: siia teha, et saata serverile asukohainfo.
    pass


def draw_everything(dt):
    global keys, colRect
    window.clear()
    batch.draw()
    batchBlock.draw()
    colRect = collidables(rect)  # who is collidable
    colSide = collisionCheck(colRect)  # checks the collision side
    update(colSide)  # updates the player movement and the scene
    fps_display.draw()
    #todo: saata serverile enda asukoht(x_player ja  y_blokide_kaugus), võibolla isegi update funktsiooni sees


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

pyglet.clock.schedule_interval(draw_everything, 1 / 90)

print(__name__)
if __name__ == 'pyglet_game_test':
    genMap()
    pyglet.app.run()
elif __name__ == '__main__':
    genMap()
    pyglet.app.run()
    # import UI
