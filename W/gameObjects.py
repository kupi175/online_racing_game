'''to create game objects'''

class atributes:
    posx=0
    posy=0
    height=0
    width=0
    def _init_(self, posx, posy, height, width):
        self.posx = posx
        self.posy = posy
        self.height = height
        self.width = width
        self.velx = 0
        self.vely = 0

    def draw(self):
        self.rect.draw()
