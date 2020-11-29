import pyglet
from pyglet.window import key, FPSDisplay, mouse
from pyglet import shapes

button_color = (148, 252, 255)
button_hover = (208, 254, 255)
button_press = (162, 216, 218)

window = pyglet.window.Window(width=1200, height=900, caption='test game', resizable=False, vsync=False )
batchMenu = pyglet.graphics.Batch()


gameButton = shapes.Rectangle(1200//2-150, 300, 300, 100, button_color, batch=batchMenu)
gameButtonState = 0

exitButton = shapes.Rectangle(1200//2-150, 100, 300, 100, button_color, batch=batchMenu)
exitButtonState = 0

exitText = pyglet.text.Label('EXIT', font_size=36, x = exitButton.x+exitButton.width//2, y = exitButton.y+exitButton.height//2, batch=batchMenu, anchor_x = 'center', anchor_y='center')
gameText = pyglet.text.Label('GAME', font_size=36, x = gameButton.x+gameButton.width//2, y = gameButton.y+gameButton.height//2, batch=batchMenu, anchor_x = 'center', anchor_y='center')

def main():
    pyglet.app.run()

def draw_everything(dt):
    global exitButtonState, gameButtonState
    if exitButtonState == 1:
        pyglet.app.exit()
    if gameButtonState == 1:
        gameButtonState = 0
        window.close()
        import pyglet_game_test
    window.clear()
    batchMenu.draw()
    exitText.draw()

@window.event
def on_draw():
    draw_everything(None)

@window.event
def on_mouse_motion(x, y, dx, dy):
    if exitButton.x < x < exitButton.x + exitButton.width:
        if exitButton.y < y < exitButton.y + exitButton.height:
            exitButton.color = button_hover
        else:
            exitButton.color = button_color
    else:
        exitButton.color = button_color

    if gameButton.x < x < gameButton.x+gameButton.width:
        if gameButton.y < y < gameButton.y+gameButton.height:
            gameButton.color = button_hover
        else:
            gameButton.color = button_color
    else:
        gameButton.color = button_color

@window.event
def on_mouse_press(x, y, button, modifiers):
    global exitButtonState, gameButtonState
    if button == pyglet.window.mouse.LEFT:
        if exitButton.x < x < exitButton.x + exitButton.width:
            if exitButton.y < y < exitButton.y + exitButton.height:
                exitButton.color = button_press
                exitButtonState = 1

    if button == pyglet.window.mouse.LEFT:
        if gameButton.x < x < gameButton.x+gameButton.width:
            if gameButton.y < y < gameButton.y+gameButton.height:
                gameButton.color = button_press
                gameButtonState = 1
@window.event
def on_mouse_release(x, y, button, modifiers):
    global exitButtonState, gameButtonState
    if button == pyglet.window.mouse.LEFT:
        if exitButton.x < x < exitButton.x + exitButton.width:
            if exitButton.y < y < exitButton.y + exitButton.height:
                exitButton.color = button_hover
                exitButtonState = 0
            else:
                exitButton.color = button_color
        else:
            exitButton.color = button_color

    if button == pyglet.window.mouse.LEFT:
        if gameButton.x < x < gameButton.x+gameButton.width:
            if gameButton.y < y < gameButton.y+gameButton.height:
                gameButton.color = button_hover
                gameButtonState = 0
            else:
                gameButton.color = button_color
        else:
            gameButton.color = button_color

#event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)
print(__name__)
pyglet.clock.schedule_interval(draw_everything, 1/120)
if __name__ == 'UI':
    main()
