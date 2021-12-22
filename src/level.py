import numpy as np

FIELD_X = 14
FIELD_Y = 10


class Level:
    def __init__(self, file):
        """
        Creates a new level object by loading the starting layout from a file and stroing it as the internal field
        :param file: The file to load the level data from
        """
        self.field = np.genfromtxt(file)
        if not self.field.shape == (FIELD_Y, FIELD_X):
            raise ValueError('File must contain a level with dimensions ' + str(FIELD_X) + "," + str(FIELD_Y))
