'''pygame test'''
import pyglet
from pyglet.window import key, FPSDisplay, mouse
from pyglet import shapes
from random import randint
import gameObjects
import Code.duplicated.map_generator as mg
#import UI

playersFail = open('players.txt').read().split('\n')  # loeb playerite asukohad
players = []
for i in playersFail:
    i= i.split(',')
    players.append(i)
playersLen = len(players)
velx = 0
vely = 0.5
ymod = 3
xmod = 2
playerRadius = 40
ver = 'alpha 0.002'

window = pyglet.window.Window(width=1200, height=900, caption='test game', resizable=False, vsync=False)
#window.set_location(650, 250)
batch = pyglet.graphics.Batch()
fps_display = FPSDisplay(window)
fps_display.label.font_size = 20
objects = players.copy()
for i in range(len(players)):
    player = shapes.Circle(int(players[1][0]), int(players[1][1]), radius=playerRadius, color=(55, 55, 255), batch=batch)

#rect = shapes.Rectangle(400, 100 ,100,500,(255,45,56), batch=batch)
#rect2 = shapes.Rectangle(0, 0,100,50,(255,255,56), batch=batch)
seed = 69420
kaart = mg.game_map(seed, 100)
kaart.get_map(start=1, end=2)
rect = []
for i in objects:
    rect.append(shapes.Rectangle(int(i[0]), int(i[1]) ,100,50,(255,255,56), batch=batch))

label = pyglet.text.Label('Py test game', font_size=26, x=window.width//2, y=window.height//2+300, anchor_x='center',
                          anchor_y='center', batch=batch)
verLabel = pyglet.text.Label(str(ver), font_size=8, x = 0, y = 0, batch=batch)

def otherPlayers(numOtherPlayers):
    global playerRadius
    otherPlayers = []
    for i in range(numOtherPlayers):
        others_radius = playerRadius
        others_x = randint(0, window.width-others_radius)
        others_y = randint(0, window.height-others_radius)
        newOtherPlayers = shapes.Circle(x = others_x, y = others_y, radius = others_radius, color = (randint(25,255), randint(25,255), randint(25,255)), batch = batch)
        otherPlayers.append(newOtherPlayers)
    return otherPlayers
otherPlayersList = otherPlayers(2)

def collision():  # vaatab, kas player on collisionis hetkel seinaga, mille nimi on rect
    global velx
    global vely
    colSide = {
        'right': False,
        'left': False,
        'down': False,
    }
    for i in rect:
        if player.y+player.radius > i.y and player.y-player.radius < i.y+i.height: #collision detection parem-vasak
            if i.x-2 < player.x+player.radius < i.x+10:
                print('left')
                colSide['left'] = True
            else:
                colSide['left'] = False
            if i.x+i.width-10 < player.x-player.radius < i.x+i.width+2:
                print('right')
                colSide['right'] = True
            else:
                colSide['right'] = False

        if i.x-2 < player.x+player.radius and player.x-player.radius < i.x+i.width+2: # alumine col.detect
            if i.y-2 < player.y + player.radius < i.y:
                print('down')
                colSide['down'] = True
            else:
                colSide['down'] = False
    #print(colSide)
    #if rect.x < player.x+player.radius and player.x-player.radius < rect.x+rect.width:
    #    if rect.y <= player.y+player.radius and player.y-player.radius <= rect.y+rect.height:
    #        velx = 0
    if colSide['right'] == True or colSide['left'] == True:
        velx = 0
        return True
    if colSide['down'] == True:
        vely = 0
        return True

        #print('collision')
            #return True
    else:
        #print('no collision')
        return False

def update(velx):
    player.x += velx
    if collision():
        player.y += 0.1

    else:
       player.y += vely
    if player.y-player.radius >= window.height:
        player.y = 0-player.radius
    if player.x >= window.width:
        player.x = 1
    if player.x < 0:
        player.x = window.width-1

def draw_everything(dt):
    window.clear()
    fps_display.draw()
    batch.draw()
    update(velx)
    collision()



@window.event
def on_draw():
    draw_everything(None)
    #print(player.y)

@window.event
def on_key_press(symbol, modifiers):
    global velx
    global vely
    global xmod
    global ymod
    if symbol == key.LEFT:
        velx -= xmod
    if symbol == key.RIGHT:
        velx += xmod
    if symbol == key.UP:
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
        vely -= 0

#event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)

pyglet.clock.schedule_interval(draw_everything, 1/120)

print(__name__)
if __name__ == 'pyglet_game_test':
    pyglet.app.run()
elif __name__ == '__main__':
    import UI