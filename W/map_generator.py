import random
from opensimplex import OpenSimplex


class game_map:
    length = None
    noise = None
    seed = None
    start_area_width = 80
    start_area_length = 10
    start_area_gradiant = 6

    def __init__(self, seed=random.randint(0, 2147483648), length=100):
        self.noise = OpenSimplex(seed=seed)
        self.seed = seed
        self.length = length * 10
        for i in range(0, self.length):
            self.generated_map = (self.noise.noise2d(i, 0) + 1) * 20  # generate a string of noise
            #print(self.generated_map)

    def get_map(self, start, end):
        ret1 = [self.get_noise_point(x, 0) for x in range(start, end)]
        ret2 = [self.get_noise_point(0, x) for x in range(start, end)]
        for x in range(start, end):
            #if x
         pass

        return tuple([ret1, ret2])

    def get_noise_point(self, x, y):
        return (self.noise.noise2d(x / 10, y / 10) + 1) / 2

    def get_seed(self):
        return self.seed
