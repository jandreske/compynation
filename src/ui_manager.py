from level import FIELD_X, FIELD_Y
import pygame as pg
import os
import directories

# Game size values
BLOCK_SIZE = 64
MENU_BLOCK_WIDTH = 4
# Dictionary for menu entries
MENU_ENTRIES = {0: "play", 1: "info", 2: "random", 3: "quit"}


class UI:
    def __init__(self):
        """
            Initializes the UI, setting the icon, title and correct window size and loading images
            """
        pg.init()
        self._menu_pics = {}
        self._images = {}
        self._tile_dict = {}
        self.load_images()
        pg.display.set_icon(self._images["logo"])
        pg.display.set_caption("Compynation")
        self._screen = pg.display.set_mode((BLOCK_SIZE * (FIELD_X + MENU_BLOCK_WIDTH), BLOCK_SIZE * FIELD_Y))
        self._clock = pg.time.Clock()
        self._selected = 0
        self._info = False
        self._random = True

    @property
    def clock(self):
        return self._clock

    @property
    def random(self):
        return self._random

    @property
    def selected(self):
        return MENU_ENTRIES[self._selected]

    def flip_info(self):
        self._info = not self._info

    def flip_random(self):
        self._random = not self._random

    def menu_up(self):
        self._selected = (self._selected - 1) % len(MENU_ENTRIES)

    def menu_down(self):
        self._selected = (self._selected + 1) % len(MENU_ENTRIES)

    def load_images(self):
        """
        Loads all images required during the game and adds references to the dictionaries IMAGES, TILE_DICT and MENU_PICS
        :return: None
        """
        self._images["info"] = pg.image.load(os.path.join(directories.GRAPHICS_DIRECTORY, "info.png"))
        self._images["logo"] = pg.image.load(os.path.join(directories.GRAPHICS_DIRECTORY, "logo.png"))
        self._images["welcome"] = pg.image.load(os.path.join(directories.GRAPHICS_DIRECTORY, "welcome.png"))
        self._images["game_marker"] = get_game_marker()
        self._images["menu_marker"] = get_menu_marker()
        for key, value in MENU_ENTRIES.items():
            self._menu_pics[key] = pg.image.load(os.path.join(directories.BUTTONS_DIRECTORY, value + ".png"))
        for tile in range(100, 107):
            self._tile_dict[tile] = pg.image.load(os.path.join(directories.TILES_DIRECTORY, str(tile) + ".gif"))
        for tile in range(1, 8):
            self._tile_dict[tile] = pg.image.load(os.path.join(directories.TILES_DIRECTORY, str(tile) + ".gif"))

    def draw_menu(self):
        """
        Draws the main menu on the screen. This includes the welcome screen or the info screen (if info is True).
        The menu buttons are being drawn as well, including the marker showing which entry is selected.
        :return: None
        """
        self._screen.fill((0xFF, 0x80, 0x00))
        if self._info:
            self._screen.blit(self._images["info"], (0, 0))
        else:
            self._screen.blit(self._images["welcome"], (0, 0))
        for entry in MENU_ENTRIES.keys():
            posx = (FIELD_X + 1) * BLOCK_SIZE
            posy = (1 + (2 * entry)) * BLOCK_SIZE
            self._screen.blit(self._menu_pics[entry], (posx, posy))
            if self._selected == entry:
                self._screen.blit(self._images["menu_marker"], (posx, posy))
        pg.display.flip()

    def draw(self, level):
        """
        Draws the elements representing the current level state on the screen.
        The numbers from the field are translated into tile images.
        :param level: the level object containing the game state data to draw
        :return: None
        """
        self._screen.fill((0x15, 0x0D, 0x09))
        for i in range(0, FIELD_Y):
            for j in range(0, FIELD_X):
                if level.field[i][j] in range(100, 107):
                    tile = self._tile_dict[level.field[i][j]]
                    self._screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                elif level.field[i][j] in range(1, 8):
                    tile = self._tile_dict[level.field[i][j]]
                    self._screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))

    def draw_marker(self, position):
        """
        Draws the marker (showing the user which block is selected) on the field.
        :param position: the position on which the marker should be drawn (block coordinates)
        :return: None
        """
        position = (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE)
        self._screen.blit(self._images["game_marker"], position)

    def show_success_screen(self, info):
        """
        Shows a screen telling the user about the successfull level completion.
        Shows which level follows next and the password to access it directly.
        Waits for user key press before returning.
        :param info: the level info object containing index and password
        :return: True if the user pressed space to continue, False if pressed escape or exited the screen
        """
        self._screen.fill((0x15, 0x0D, 0x09))
        text = ["Yay, you made it!",
                "Next Level: " + str(info.index),
                "Password: " + info.password,
                "Press space to continue"]
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    elif event.key == pg.K_SPACE:
                        return True

    def show_password_screen(self):
        """
        Shows the enter password screen. Allows for the user to type a password in order to access later levels.
        :return: The password entered by the user
        """
        self._screen.fill((0x15, 0x0D, 0x09))
        password = ""
        text = ["Enter the level password.",
                "Leave empty to start with first level.",
                "Password: ",
                password]
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(60)
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
            self._screen.fill((0x15, 0x0D, 0x09))
            self.write_text(text, x, y)
            pg.display.flip()

    def write_text(self, text, x, y):
        """
        Helper function to write multiple lines of text on the screen.
        Each new lines starts one Block size lower.
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
            self._screen.blit(text_image, text_rect)


def get_game_marker():
    """
    Loads the game marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = pg.image.load(os.path.join(directories.GRAPHICS_DIRECTORY, "game_marker.png"))
    marker.set_colorkey((0, 0, 0))
    return marker


def get_menu_marker():
    """
    Loads the menu marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = pg.image.load(os.path.join(directories.GRAPHICS_DIRECTORY, "menu_marker.png"))
    marker.set_colorkey((0, 0, 0))
    return marker
