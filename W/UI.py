import pyglet
from pyglet.window import key, FPSDisplay, mouse
from pyglet import shapes
from random import randint

button_color = (148, 252, 255)
button_hover = (208, 254, 255)
button_press = (162, 216, 218)

window = pyglet.window.Window(width=1200, height=900, caption='test game', resizable=False, vsync=False )
batchMenu = pyglet.graphics.Batch()
exitButton = shapes.Rectangle(1200//2-150, 100, 300, 100, button_color, batch=batchMenu)
exitButtonState = 0
exitText = pyglet.text.Label('EXIT', font_size=36, x = exitButton.x+exitButton.width//2, y = exitButton.y+exitButton.height//2, batch=batchMenu, anchor_x = 'center', anchor_y='center')

def draw_everything(dt):
    global exitButtonState
    if exitButtonState == 1:
        pyglet.app.exit()
    window.clear()
    batchMenu.draw()
    exitText.draw()

@window.event
def on_draw():
    draw_everything(None)

@window.event
def on_mouse_motion(x, y, dx, dy):
    if exitButton.x < x < exitButton.x+exitButton.width:
        if exitButton.y < y < exitButton.y+exitButton.height:
            exitButton.color = button_hover
        else:
            exitButton.color = button_color
    else:
        exitButton.color = button_color

@window.event
def on_mouse_press(x, y, button, modifiers):
    global exitButtonState
    if button == pyglet.window.mouse.LEFT:
        if exitButton.x < x < exitButton.x+exitButton.width:
            if exitButton.y < y < exitButton.y+exitButton.height:
                exitButton.color = button_press
                exitButtonState = 1
@window.event
def on_mouse_release(x, y, button, modifiers):
    global exitButtonState
    if button == pyglet.window.mouse.LEFT:
        if exitButton.x < x < exitButton.x + exitButton.width:
            if exitButton.y < y < exitButton.y + exitButton.height:
                exitButton.color = button_hover
                exitButtonState = 0
            else:
                exitButton.color = button_color
        else:
            exitButton.color = button_color

event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)

pyglet.clock.schedule_interval(draw_everything, 1/120)
if __name__ == '__main__':
    pyglet.app.run()