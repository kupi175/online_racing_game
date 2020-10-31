import random
from opensimplex import OpenSimplex


class game_map:
    type = None
    lap_count = None
    generated_map = []
    length = None
    noise = None

    def __init__(self, seed=random.randint(0, 2147483648), type='Straight', laps=None, length=100):
        self.noise = OpenSimplex(seed=seed)
        self.length = length
        for i in range(0, self.length):
            self.generated_map = (self.noise.noise2d(i, 0)+1)*20 # generate a string of noise
            print(self.generated_map)
