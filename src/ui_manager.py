from level import FIELD_X, FIELD_Y
import pygame as pg
import os
import directories

# Game size values
BLOCK_SIZE = 64
MENU_BLOCK_WIDTH = 4
NUMBER_WIDTH = 34
TIME_X = FIELD_X * BLOCK_SIZE + 100
TIME_Y = 110
SCORE_X = FIELD_X * BLOCK_SIZE + 65
SCORE_Y = 315
LEVEL_X = FIELD_X * BLOCK_SIZE + 100
LEVEL_Y = 475
# Tile image values
MOVE_MIN_TILE = 1
MOVE_MAX_TILE = 15
BACK_DEFAULT_TILE = 100
BACK_MIN_TILE = 100
BACK_MAX_TILE = 117
# Dictionary for menu entries
MENU_ENTRIES = {0: "play", 1: "info", 2: "password", 3: "lives", 4: "time", 5: "music", 6: "random", 7: "highscores"}
# User interaction values
FRAMERATE = 60
STABILIZING_FRAMERATE = 4
# Colors
BACKGROUND_COLOR = (0x15, 0x0D, 0x09)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class UI:
    def __init__(self):
        """
            Initializes the UI, setting the icon, title and correct window size and loads images
            """
        pg.init()
        self._menu_pics = {}
        self._images = {}
        self._tile_dict = {}
        self._game_menues = {}
        self._numbers = {}
        self._gm = 3
        self.load_images()
        pg.display.set_icon(self._images["logo"])
        pg.display.set_caption("Compynation")
        self._screen = pg.display.set_mode((BLOCK_SIZE * (FIELD_X + MENU_BLOCK_WIDTH), BLOCK_SIZE * FIELD_Y))
        self._clock = pg.time.Clock()
        self._selected = 0
        self._info = False
        self._random = True
        self._lives = True
        self._time = True
        self._music = True

    @property
    def clock(self):
        return self._clock

    @property
    def random(self):
        return self._random

    @property
    def selected(self):
        return MENU_ENTRIES[self._selected]

    @property
    def lives(self):
        return self._lives

    @property
    def time(self):
        return self._time

    @property
    def music(self):
        return self._music

    def flip_info(self):
        self._info = not self._info

    def flip_random(self):
        self._random = not self._random

    def flip_lives(self):
        self._lives = not self._lives

    def flip_time(self):
        self._time = not self._time

    def flip_music(self):
        self._music = not self._music

    def menu_up(self):
        self._selected = (self._selected - 1) % len(MENU_ENTRIES)

    def menu_down(self):
        self._selected = (self._selected + 1) % len(MENU_ENTRIES)

    def set_game_menu(self, lives):
        self._gm = lives

    def load_images(self):
        """
        Loads all images required during the game and adds references to the dictionaries
        IMAGES, TILE_DICT and MENU_PICS
        :return: None
        """
        self._images["info"] = load_image(directories.GENERAL_DIRECTORY, "info.png")
        self._images["logo"] = load_image(directories.GENERAL_DIRECTORY, "logo.png")
        self._images["welcome"] = load_image(directories.GENERAL_DIRECTORY, "welcome.png")
        self._images["game_marker"] = get_game_marker()
        self._images["menu_marker"] = get_menu_marker()
        self._game_menues[1] = load_image(directories.GENERAL_DIRECTORY, "game_menu_1.png")
        self._game_menues[2] = load_image(directories.GENERAL_DIRECTORY, "game_menu_2.png")
        self._game_menues[3] = load_image(directories.GENERAL_DIRECTORY, "game_menu_3.png")
        for key, value in MENU_ENTRIES.items():
            self._menu_pics[key] = load_image(directories.BUTTONS_DIRECTORY, value + ".png")
        for tile in range(BACK_MIN_TILE, BACK_MAX_TILE + 1):
            self._tile_dict[tile] = load_image(directories.TILES_DIRECTORY, str(tile) + ".gif")
        for tile in range(MOVE_MIN_TILE, MOVE_MAX_TILE + 1):
            self._tile_dict[tile] = load_image(directories.TILES_DIRECTORY, str(tile) + ".gif")
        for number in range(0, 10):
            self._numbers[number] = load_image(directories.NUMBERS_DIRECTORY, str(number) + ".gif")

    def draw_menu(self):
        """
        Draws the main menu on the screen. This includes the welcome screen or the info screen (if info is True).
        The menu buttons are being drawn as well, including the marker showing which entry is selected.
        :return: None
        """
        self._screen.fill(BACKGROUND_COLOR)
        if self._info:
            self._screen.blit(self._images["info"], (0, 0))
        else:
            self._screen.blit(self._images["welcome"], (0, 0))
        for entry in MENU_ENTRIES.keys():
            posx = (FIELD_X + 1) * BLOCK_SIZE
            posy = (1 + (1.5 * entry)) * BLOCK_SIZE
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
        self._screen.fill(BACKGROUND_COLOR)
        for i in range(0, FIELD_Y):
            for j in range(0, FIELD_X):
                if level.field[i][j] in range(BACK_MIN_TILE, BACK_MAX_TILE + 1):
                    tile = self._tile_dict[level.field[i][j]]
                    self._screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                elif level.field[i][j] in range(MOVE_MIN_TILE, MOVE_MAX_TILE + 1):
                    tile = self._tile_dict[level.field[i][j]]
                    self._screen.blit(tile, (j * BLOCK_SIZE, i * BLOCK_SIZE))

    def draw_game_menu(self, level, score, time_left):
        """
        Draws the right hand side game menu with lives, score, time and level info
        :param level: which level is being played
        :param score: the curretn total score
        :param time_left: the time left during this level
        :return: None
        """
        image = self._game_menues[self._gm]
        self._screen.blit(image, (FIELD_X * BLOCK_SIZE, 0))
        self.write_number(time_left, 2, TIME_X, TIME_Y)
        self.write_number(level, 2, LEVEL_X, LEVEL_Y)
        self.write_number(score, 4, SCORE_X, SCORE_Y)

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
        Shows a screen telling the user about the successfull level completion and the achieved points.
        Shows which level follows next and the password to access it directly.
        Waits for user key press before returning.
        :param info: the level info object containing index, password and points
        :return: True if the user pressed space to continue, False if pressed escape or exited the screen
        """
        self._screen.fill(BACKGROUND_COLOR)
        text = ["Yay, you made it!",
                "Score achieved: " + str(info.last_score),
                "Time bonus: " + str(info.time_score),
                "Total points: " + str(info.total_score),
                "Next Level: " + str(info.index),
                "Password: " + info.password,
                "Press space to continue"]
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    elif event.key == pg.K_SPACE:
                        return True

    def show_winning_screen(self, info):
        """
        Shows a screen telling the user he completed the game, and shows the achieved points
        :param info: the level info object containing score data
        :return: None
        """
        self._screen.fill(BACKGROUND_COLOR)
        text = ["Awesome, you completed the game!",
                "Score achieved: " + str(info.last_score),
                "Time bonus: " + str(info.time_score),
                "Bonus points for remaining lives: " + str(info.bonus_score),
                "Total points: " + str(info.total_score),
                "Press space to continue"]
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                    return

    def show_highscores(self, highscores):
        """
        Shows the highscores
        :param highscores: dictionary containing highscore entries
        :return: None
        """
        self._screen.fill(BACKGROUND_COLOR)
        text = ["Highscores"]
        for score in sorted(highscores, reverse=True):
            text.append(str(score) + " - " + highscores[score])
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                    return

    def show_failure_screen(self, lives):
        """
        Shows a screen informing the user a level attempt has failed
        :param lives: number of lives the user has left
        :return: True if the user wants to and can continue playing, False otherwise
        """
        self._screen.fill(BACKGROUND_COLOR)
        text = ["Oh no, that did not work out.",
                "Lives left: " + str(lives),
                "Press space to try again."]
        if lives < 1:
            text[2] = "Press space to return to the menu."
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    elif event.key == pg.K_SPACE:
                        return lives > 0

    def show_password_screen(self):
        """
        Shows the enter password screen. Allows for the user to type a password in order to access later levels.
        :return: The password entered by the user
        """
        self._screen.fill(BACKGROUND_COLOR)
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
            self._clock.tick(FRAMERATE)
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
            self._screen.fill(BACKGROUND_COLOR)
            self.write_text(text, x, y)
            pg.display.flip()

    def get_user_name(self):
        """
        Shows the enter username screen. Allows for the user to type a name for the highscore list.
        :return: The name entered by the user
        """
        self._screen.fill(BACKGROUND_COLOR)
        name = ""
        text = ["Enter your name for the highscore list.",
                "Name: ",
                name]
        x = BLOCK_SIZE * 4
        y = BLOCK_SIZE * 2
        self.write_text(text, x, y)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return name
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return name
                    elif event.unicode.isalpha():
                        name = name + event.unicode.upper()
                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pg.K_RETURN:
                        return name
            text[2] = name
            self._screen.fill(BACKGROUND_COLOR)
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
            text_image = font.render(text[i], True, WHITE)
            text_rect = text_image.get_rect()
            text_rect.x = x
            text_rect.y = y + i * BLOCK_SIZE
            self._screen.blit(text_image, text_rect)

    def write_number(self, number, length, x, y):
        """
        "writes" a number onto the screen using images for the digits
        :param number: the number to display
        :param length: number of digits to show (if the number is too big, lower digits are used)
        :param x: x position to start dispalying at
        :param y: y position to start displaying at
        :return: None
        """
        for i in range(0, length):
            digit = (number % (10**(length - i))) // (10**(length - i - 1))
            image = self._numbers[digit]
            position = (x + i * NUMBER_WIDTH, y)
            self._screen.blit(image, position)


def get_game_marker():
    """
    Loads the game marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = load_image(directories.GENERAL_DIRECTORY, "game_marker.png")
    marker.set_colorkey(BLACK)
    return marker


def get_menu_marker():
    """
    Loads the menu marker image and sets the background to transparent
    :return: The loaded image containing the marker with transparent background
    """
    marker = load_image(directories.GENERAL_DIRECTORY, "menu_marker.png")
    marker.set_colorkey(BLACK)
    return marker


def load_image(directory, file):
    """
    Loads an image using the PyGame load function
    :param directory: directory where the image is located
    :param file: name of the image file
    :return: The image object holding the loaded image
    """
    return pg.image.load(os.path.join(directory, file))
