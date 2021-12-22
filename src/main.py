from level import Level, FIELD_X, FIELD_Y
import pygame as pg

LEVEL_DIRECTORY = "levels/"
GRAPHICS_DIRECTORY = "graphics/"
BLOCK_SIZE = 64
COLOR_DICT = {0: (255, 255, 255), 100: (102, 0, 51), 101: (153, 0, 76), 102: (204, 0, 102),
              1: (51, 255, 51), 2: (51, 51, 255), 3: (255, 51, 51)}


def init():
    """
    Initializes the UI, setting the icon, title and correct window size
    :return: a pygame surface element used as screen for the game
    """
    pg.init()
    logo = pg.image.load(GRAPHICS_DIRECTORY + "logo.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("Compynation")
    screen = pg.display.set_mode((BLOCK_SIZE * FIELD_X, BLOCK_SIZE * FIELD_Y))
    return screen


def draw(screen, level):
    """
    Draws the elements representing the current level state on the screen.
    The numbers from the level.field member are translated into colors for the blocks.
    The static block size is sued to determine recttangle size on the screen
    :param screen: the screen to draw the level on
    :param level: the level object containing the game state data to draw
    :return: None
    """
    screen.fill((0xFF, 0x80, 0x00))
    for i in range(0, FIELD_Y):
        for j in range(0, FIELD_X):
            color = COLOR_DICT[level.field[i][j]]
            pg.draw.rect(screen, color, pg.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
    """
    Main entry point into the game, this function initializes everything and then executes the main loop
    :return: None
    """
    screen = init()
    level = Level(LEVEL_DIRECTORY + "level_01")
    draw(screen, level)
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == "__main__":
    main()
