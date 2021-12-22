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


def draw_marker(screen, marker, position):
    position = (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE)
    screen.blit(marker, position)


def get_marker():
    marker = pg.image.load(GRAPHICS_DIRECTORY + "marker.png")
    marker.set_colorkey((0, 0, 0))
    return marker


def main():
    """
    Main entry point into the game, this function initializes everything and then executes the main loop
    :return: None
    """
    screen = init()
    level = Level(LEVEL_DIRECTORY + "level_01")
    draw(screen, level)
    position = (0, 0)
    marker = get_marker()
    draw_marker(screen, marker, position)
    pg.display.flip()
    clock = pg.time.Clock()
    running = True
    while running:
        clock.tick(60)
        newpos = position
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    newpos = (newpos[0], max(0, newpos[1] - 1))
                elif event.key == pg.K_DOWN:
                    newpos = (newpos[0], min(FIELD_Y - 1, newpos[1] + 1))
                elif event.key == pg.K_LEFT:
                    newpos = (max(0, newpos[0] - 1), newpos[1])
                    if pg.key.get_pressed()[pg.K_SPACE]:
                        if level.move(position, -1):
                            break
                elif event.key == pg.K_RIGHT:
                    newpos = (min(FIELD_X - 1, newpos[0] + 1), newpos[1])
                    if pg.key.get_pressed()[pg.K_SPACE]:
                        if level.move(position, +1):
                            break
        position = newpos
        draw(screen, level)
        draw_marker(screen, marker, position)
        pg.display.flip()
        while not level.stable:
            clock.tick(60)
            level.stabilize()
            draw(screen, level)
            draw_marker(screen, marker, position)
            pg.display.flip()


if __name__ == "__main__":
    main()
