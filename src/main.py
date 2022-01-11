from level import Level, FIELD_X, FIELD_Y
import pygame as pg
import os

# Directories for images and level data
from level_info import LevelInfo

DIRNAME = os.path.abspath(os.path.dirname(__file__))
LEVEL_DIRECTORY = os.path.join(DIRNAME, "levels")
GRAPHICS_DIRECTORY = os.path.join(DIRNAME, "graphics")
BUTTONS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "buttons")
TILES_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "tiles")
# Game size values
BLOCK_SIZE = 64
MENU_BLOCK_WIDTH = 4
# Dictionaries for images, menu entries, tiles and levels
MENU_ENTRIES = {0: "play", 1: "info", 2: "random", 3: "quit"}
MENU_PICS = {}
IMAGES = {}
TILE_DICT = {}
LEVEL_PASSWORDS = {}
LEVEL_FILES = {}


def main():
    """
    Main entry point into the game, this function initializes everything and then runs the main menu loop
    :return: None
    """
    screen = init()
    clock = pg.time.Clock()
    selected = 0
    info = False
    random = True
    draw_menu(screen, selected, info)
    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    selected = (selected - 1) % len(MENU_ENTRIES)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(MENU_ENTRIES)
                elif event.key == pg.K_SPACE:
                    choice = MENU_ENTRIES[selected]
                    if choice == "quit":
                        running = False
                    elif choice == "info":
                        info = not info
                    elif choice == "random":
                        random = not random
                    elif choice == "play":
                        play_game(screen, clock, random)
                draw_menu(screen, selected, info)


def init():
    """
    Initializes the UI, setting the icon, title and correct window size
    :return: a pygame surface element used as screen for the game
    """
    pg.init()
    load_images()
    pg.display.set_icon(IMAGES["logo"])
    pg.display.set_caption("Compynation")
    screen = pg.display.set_mode((BLOCK_SIZE * (FIELD_X + MENU_BLOCK_WIDTH), BLOCK_SIZE * FIELD_Y))
    return screen


def load_images():
    """
    Loads all images required during the game and adds references to the dictionaries IMAGES, TILE_DICT and MENU_PICS
    :return: None
    """
    IMAGES["info"] = pg.image.load(os.path.join(GRAPHICS_DIRECTORY, "info.png"))
    IMAGES["logo"] = pg.image.load(os.path.join(GRAPHICS_DIRECTORY, "logo.png"))
    IMAGES["welcome"] = pg.image.load(os.path.join(GRAPHICS_DIRECTORY, "welcome.png"))
    IMAGES["game_marker"] = get_game_marker()
    IMAGES["menu_marker"] = get_menu_marker()
    for key, value in MENU_ENTRIES.items():
        MENU_PICS[key] = pg.image.load(os.path.join(BUTTONS_DIRECTORY, value + ".png"))
    for tile in range(100, 107):
        TILE_DICT[tile] = pg.image.load(os.path.join(TILES_DIRECTORY, str(tile) + ".gif"))
    for tile in range(1, 8):
        TILE_DICT[tile] = pg.image.load(os.path.join(TILES_DIRECTORY, str(tile) + ".gif"))


def draw_menu(screen, selected, showinfo):
    """
    Draws the main menu on the screen. This includes the welcome screen or the info screen (if info is True).
    The menu buttons are being drawn as well, including the marker showing which entry is selected.
    :param screen: The surface to draw on
    :param selected: index of the selected menu entry
    :param showinfo: whether the info screen should be shown (instead of welcome screen)
    :return: None
    """
    screen.fill((0xFF, 0x80, 0x00))
    if showinfo:
        screen.blit(IMAGES["info"], (0, 0))
    else:
        screen.blit(IMAGES["welcome"], (0, 0))
    for entry in MENU_ENTRIES.keys():
        posx = (FIELD_X + 1) * BLOCK_SIZE
        posy = (1 + (2 * entry)) * BLOCK_SIZE
        screen.blit(MENU_PICS[entry], (posx, posy))
        if selected == entry:
            screen.blit(IMAGES["menu_marker"], (posx, posy))
    pg.display.flip()


def draw(screen, level):
    """
    Draws the elements representing the current level state on the screen.
    The numbers from the field are translated into tile images.
    :param screen: the screen to draw the level on
    :param level: the level object containing the game state data to draw
    :return: None
    """
    screen.fill((0x15, 0x0D, 0x09))
    for i in range(0, FIELD_Y):
        for j in range(0, FIELD_X):
            if level.field[i][j] in range(100, 107):
                tile = TILE_DICT[level.field[i][j]]
                screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))
            elif level.field[i][j] in range(1, 8):
                tile = TILE_DICT[level.field[i][j]]
                screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))


def draw_marker(screen, position):
    """
    Draws the marker (showing the user which block is selected) on the field.
    :param screen: The screen to draw on
    :param position: the position on which the marker should be drawn (block coordinates)
    :return: None
    """
    position = (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE)
    screen.blit(IMAGES["game_marker"], position)


def get_game_marker():
    """
    Loads the game marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = pg.image.load(os.path.join(GRAPHICS_DIRECTORY, "game_marker.png"))
    marker.set_colorkey((0, 0, 0))
    return marker


def get_menu_marker():
    """
    Loads the menu marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = pg.image.load(os.path.join(GRAPHICS_DIRECTORY, "menu_marker.png"))
    marker.set_colorkey((0, 0, 0))
    return marker


def load_level(name):
    """
    Loads a level from a file
    :param name: the name of the level file in the levels directory
    :return: The Level object constructed from the file content
    """
    return Level(os.path.join(LEVEL_DIRECTORY, name))


def show_success_screen(screen, clock, info):
    """
    Shows a screen telling the user about the successfull level completion.
    Shows which level follows next and the password to access it directly.
    Waits for user key press before returning.
    :param screen: The pygame surface to draw on
    :param clock: The pygame clock
    :param info: The levelinfo object for the following level
    :return: True if the user pressed space to continue, False if pressed escape or exited the screen
    """
    screen.fill((0x15, 0x0D, 0x09))
    text = ["Yay, you made it!",
            "Next Level: " + str(info.index),
            "Password: " + info.password,
            "Press space to continue"]
    x = BLOCK_SIZE * 4
    y = BLOCK_SIZE * 2
    write_text(screen, text, x, y)
    pg.display.flip()
    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                elif event.key == pg.K_SPACE:
                    return True


def show_password_screen(screen, clock):
    """
    Shows the enter password screen. Allows for the user to type a password in order to access later levels.
    :param screen: Pygame surface to draw on
    :param clock: Pygame clock used for the framerate (for checking user keystrokes)
    :return: The password entered by the user
    """
    screen.fill((0x15, 0x0D, 0x09))
    password = ""
    text = ["Enter the level password.",
            "Leave empty to start with first level.",
            "Password: ",
            password]
    x = BLOCK_SIZE * 4
    y = BLOCK_SIZE * 2
    write_text(screen, text, x, y)
    pg.display.flip()
    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return password
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return password
                elif event.unicode.isalpha():
                    password = password + event.unicode.upper()
                elif event.key == pg.K_BACKSPACE:
                    password = password[:-1]
                elif event.key == pg.K_RETURN:
                    return password
        text[3] = password
        screen.fill((0x15, 0x0D, 0x09))
        write_text(screen, text, x, y)
        pg.display.flip()


def write_text(screen, text, x, y):
    """
    Helper function to write multiple lines of text on the screen.
    Each new lines starts one Block size lower.
    :param screen: Surface to write on
    :param text: List of text lines to render
    :param x: x coordinate for upper left corner
    :param y: y coordinate for upper left corner
    :return: None
    """
    font = pg.font.Font(None, 30)
    for i in range(0, len(text)):
        text_image = font.render(text[i], True, (255, 255, 255))
        text_rect = text_image.get_rect()
        text_rect.x = x
        text_rect.y = y + i * BLOCK_SIZE
        screen.blit(text_image, text_rect)


def play_game(screen, clock, random):
    """
    Organizes the sequence of levels to play. Loads the level info from a file, allows user password input
    and manages info screens in between solved or failed levels
    :param screen: Surface to draw on
    :param clock: Clock for setting interaction frame rate
    :param random: whether level tiles should be randomized (appearance only)
    :return: None
    """
    info = LevelInfo(os.path.join(LEVEL_DIRECTORY, "list.txt"))
    password = show_password_screen(screen, clock)
    level = load_level(info.by_password(password))
    playing = True
    while playing:
        if play_level(screen, clock, level, random):
            next_level = info.next
            if not next_level:
                # winning screen
                playing = False
            else:
                if show_success_screen(screen, clock, info):
                    level = load_level(next_level)
                else:
                    playing = False
        else:
            # Leben checken, fragen ob weiter spielen?
            playing = False
    # punkte anzeigen etc, highscore


def play_level(screen, clock, level, random):
    """
    Loads a level and then runs the loop to play the game, allowing the user to make moves.
    :param random: whether the tile images should be randomized
    :param level: the level object containing the initial game state
    :param screen: The surface to draw on
    :param clock: The game clock used to adjust frame rates
    :return: True if the level was cleared, False otherwise
    """
    if random:
        level.randomize(1, 7, 100, 106, 100)
    draw(screen, level)
    position = (0, 0)
    draw_marker(screen, position)
    pg.display.flip()
    while True:
        clock.tick(60)
        new_position = position
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                elif event.key == pg.K_UP:
                    new_position = (new_position[0], max(0, new_position[1] - 1))
                elif event.key == pg.K_DOWN:
                    new_position = (new_position[0], min(FIELD_Y - 1, new_position[1] + 1))
                elif event.key == pg.K_LEFT:
                    new_position = (max(0, new_position[0] - 1), new_position[1])
                    if pg.key.get_pressed()[pg.K_SPACE]:
                        if level.move(position, -1):
                            break
                elif event.key == pg.K_RIGHT:
                    new_position = (min(FIELD_X - 1, new_position[0] + 1), new_position[1])
                    if pg.key.get_pressed()[pg.K_SPACE]:
                        if level.move(position, +1):
                            break
        if position != new_position:
            position = new_position
            draw(screen, level)
            draw_marker(screen, position)
            pg.display.flip()
            while not level.stable:
                clock.tick(4)
                level.stabilize()
                draw(screen, level)
                draw_marker(screen, position)
                pg.display.flip()
            if level.solved:
                return True


if __name__ == "__main__":
    main()
