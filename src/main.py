from level import Level, FIELD_X, FIELD_Y
import pygame as pg

LEVEL_DIRECTORY = "levels/"
GRAPHICS_DIRECTORY = "graphics/"
BLOCK_SIZE = 64
COLOR_DICT = {0: (255, 255, 255), 100: (102, 0, 51), 101: (153, 0, 76), 102: (204, 0, 102),
              1: (51, 255, 51), 2: (51, 51, 255), 3: (255, 51, 51)}


def init():
    pg.init()
    logo = pg.image.load(GRAPHICS_DIRECTORY + "logo.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("Compynation")
    screen = pg.display.set_mode((BLOCK_SIZE * FIELD_X, BLOCK_SIZE * FIELD_Y))
    return screen


def draw(screen, level):
    screen.fill((0xFF, 0x80, 0x00))
    for i in range(0, FIELD_Y):
        for j in range(0, FIELD_X):
            color = COLOR_DICT[level.field[i][j]]
            pg.draw.rect(screen, color, pg.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
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
