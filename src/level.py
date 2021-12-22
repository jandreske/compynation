import numpy as np

FIELD_X = 14
FIELD_Y = 10


def has_matching_neigbour(field, position):
    x = position[0]
    y = position[1]
    # check above
    if (y > 0) and (abs(field[y][x]) == abs(field[y - 1][x])):
        return True
    # check below
    if (y < FIELD_Y - 1) and (abs(field[y][x]) == abs(field[y + 1][x])):
        return True
    # check left
    if (x > 0) and (abs(field[y][x]) == abs(field[y][x - 1])):
        return True
    # check above
    if (x < FIELD_X - 1) and (abs(field[y][x]) == abs(field[y][x + 1])):
        return True
    # no matches
    return False


class Level:
    def __init__(self, file):
        """
        Creates a new level object by loading the starting layout from a file and storing it as the internal field.
        If the shape does not match the expected dimensions, an exception is raised.
        :param file: The file to load the level data from
        """
        self._field = np.genfromtxt(file)
        self._stable = True
        if not self.field.shape == (FIELD_Y, FIELD_X):
            raise ValueError('File must contain a level with dimensions ' + str(FIELD_X) + "," + str(FIELD_Y))

    @property
    def field(self):
        return self._field

    @property
    def stable(self):
        return self._stable

    def move(self, position, direction):
        if not ((direction == -1) or (direction == 1)):
            return False
        x = position[0]
        y = position[1]
        if x < 0 or x >= FIELD_X or y < 0 or y >= FIELD_Y:
            return False
        if not (0 < self._field[y][x] < 100):
            return False
        target_x = x + direction
        if target_x < 0 or target_x >= FIELD_X:
            return False
        if self._field[y][target_x] != 0:
            return False
        self._field[y][target_x] = self._field[y][x]
        self._field[y][x] = 0
        self._stable = False
        return True

    def stabilize(self):
        if self._stable:
            return True
        falling = False
        for y in range(FIELD_Y - 2, -1, -1):
            for x in range(0, FIELD_X):
                if (0 < self._field[y][x] < 100) and (self._field[y+1][x] == 0):
                    falling = True
                    self._field[y + 1][x] = self._field[y][x]
                    self._field[y][x] = 0
        if falling:
            return False
        exploding = False
        for x in range(0, FIELD_X):
            for y in range(0, FIELD_Y):
                if (0 < self._field[y][x] < 100) and has_matching_neigbour(self._field, (x, y)):
                    exploding = True
                    self._field[y][x] = -1 * abs(self._field[y][x])
        self._field[self._field < 0] = 0
        if exploding:
            return False
        self._stable = True
        return True

