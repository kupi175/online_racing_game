

class playerAtributes:
    def _init_(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0

    def draw(self):
        self.rect.draw()
