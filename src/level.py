import numpy as np

FIELD_X = 14
FIELD_Y = 10


class Level:
    def __init__(self, file):
        self.field = np.genfromtxt(file)
