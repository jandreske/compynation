import random
import numpy as np

FIELD_X = 14
FIELD_Y = 10
DEFAULT_BACKGROUND_PERCENTAGE = 0.7


class Level:
    def __init__(self, file):
        """
        Creates a new level object by loading the starting layout from a file and storing it as the internal field.
        If the shape does not match the expected dimensions, an exception is raised.
        :param file: The file to load the level data from
        """
        self._field = np.genfromtxt(file)
        self._stable = False
        self._score = 0
        if not self.field.shape == (FIELD_Y, FIELD_X):
            raise ValueError('File must contain a level with dimensions ' + str(FIELD_X) + "," + str(FIELD_Y))
        self._movable = np.count_nonzero((self._field < 100) & (self._field > 0))
        if not self.stabilize():
            raise ValueError('Field needs to be stable at start')

    @property
    def field(self):
        return self._field

    @property
    def stable(self):
        return self._stable

    @property
    def solved(self):
        return self._movable == 0

    @property
    def score(self):
        return self._score

    def move(self, position, direction):
        """
        Moves a block on position to the left or right, if it is movable and the target field is empty
        :param position: coordinates of the block to be moved
        :param direction: -1 to move left or +1 to move right
        :return: True if the block was moved, false if not
        """
        if not self._stable:
            return False
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
        """
        If the field is not stable (if blocks are falling or next to matching blocks) one step towards a stable
        situations is being made. That means if blocks are falling, all falling blocks move one field down. If no
        blocks are falling, those next to matching neighbours disappear.
        :return: True if nothing happened and the field is now stable, false if changes happened
        """
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
                if (0 < self._field[y][x] < 100) and has_matching_neighbour(self._field, (x, y)):
                    exploding = True
                    self._field[y][x] = -1 * abs(self._field[y][x])
        blocks_removed = np.count_nonzero(self._field < 0)
        if blocks_removed > 0:
            self._movable = self._movable - blocks_removed
            self._score = self._score + get_score(blocks_removed)
            self._field[self._field < 0] = 0
        if exploding:
            return False
        self._stable = True
        return True

    def add_score(self, points):
        """
        Used to count up the points achieved so far
        :param points: how many points to add
        :return: None
        """
        self._score = self._score + points

    def randomize(self, min_move, max_move, min_back, max_back, default_back):
        """
        Shuffles the tile values, maintaining type (background or movable) and keeps movable pairs
        This allows graphics to vary while maintaining the same game mechanics
        :param min_move: minimum ID of the movable tiles images
        :param max_move: maximum ID of the movable tiles images
        :param min_back: minimum background tile ID
        :param max_back: maximum background tile ID
        :param default_back: ID of the main background tile (will be used for 70% of background blocks)
        :return: None
        """
        offset = random.randrange(min_move, max_move)
        for y in range(0, FIELD_Y):
            for x in range(0, FIELD_X):
                if self._field[y][x] in range(min_move, max_move + 1):
                    self._field[y][x] = min_move + ((self._field[y][x] + offset) % (max_move - min_move + 1))
                if self._field[y][x] in range(min_back, max_back + 1):
                    tile = random.randrange(min_back, max_back + 1)
                    if random.random() < DEFAULT_BACKGROUND_PERCENTAGE:
                        tile = default_back
                    self._field[y][x] = tile


def get_score(blocks_removed):
    """
    Returns the score for a certain number of removed blocks
    :param blocks_removed: how many blocks were removed
    :return: The number of points which should get awarded
    """
    if blocks_removed < 2:
        raise ValueError("Invalid number of removed blocks: " + str(blocks_removed))
    if blocks_removed == 2:
        return 20
    if blocks_removed == 3:
        return 40
    return blocks_removed * 15


def has_matching_neighbour(field, position):
    """
    Checks whether a given position on a playing field contains a movable block next to a matching same block
    :param field: The field containing all blocks
    :param position: The position to check
    :return: True if the position has a matching neighbour, false otherwise
    """
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
    # check right
    if (x < FIELD_X - 1) and (abs(field[y][x]) == abs(field[y][x + 1])):
        return True
    # no matches
    return False
