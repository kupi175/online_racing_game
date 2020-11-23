import random
from opensimplex import OpenSimplex


class game_map:
    type = None
    length = None
    noise = None
    resolution = 1

    def __init__(self, seed=random.randint(0, 2147483648), type='point_to_point', length=100, resolution = 1):
        self.noise = OpenSimplex(seed=seed)
        self.length = length
        self.type = type
        self.resolution = resolution
        for i in range(0, self.length):
            self.generated_map = (self.noise.noise2d(i, 0)+1)*20 # generate a string of noise
            print(self.generated_map)

    def get_map(self,start,end):
        pass
