import pygame as pg
import os
import directories
from game_constants import *


class UI:
    def __init__(self):
        """
            Initializes the UI, setting the icon, title and correct window size and loads images
            """
        pg.init()
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
        :return: None
        """
        self._images["info"] = load_image(directories.GENERAL_DIRECTORY, "info.png")
        self._images["logo"] = load_image(directories.GENERAL_DIRECTORY, "logo.png")
        self._images["welcome"] = load_image(directories.GENERAL_DIRECTORY, "welcome.png")
        self._images["placeholder"] = load_image(directories.GENERAL_DIRECTORY, "placeholder.png")
        self._images["game_marker"] = get_game_marker()
        self._images["sidebar_menu"] = load_image(directories.MENU_DIRECTORY, "sidebarmenu.png")
        self._images["lives"] = load_image(directories.MENU_DIRECTORY, "lives.png")
        self._images["time"] = load_image(directories.MENU_DIRECTORY, "time.png")
        self._images["random"] = load_image(directories.MENU_DIRECTORY, "random.png")
        self._images["music"] = load_image(directories.MENU_DIRECTORY, "music.png")
        self._images["menu_marker"] = load_image(directories.MENU_DIRECTORY, "marker.gif")
        self._game_menues[0] = load_image(directories.MENU_DIRECTORY, "game_menu_0.png")
        self._game_menues[1] = load_image(directories.MENU_DIRECTORY, "game_menu_1.png")
        self._game_menues[2] = load_image(directories.MENU_DIRECTORY, "game_menu_2.png")
        self._game_menues[3] = load_image(directories.MENU_DIRECTORY, "game_menu_3.png")
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
        self._screen.blit(self._images["sidebar_menu"], (FIELD_X * BLOCK_SIZE, 0))
        if self._lives:
            self._screen.blit(self._images["lives"], POS_LIVES)
        if self._time:
            self._screen.blit(self._images["time"], POS_TIME)
        if self._random:
            self._screen.blit(self._images["random"], POS_RANDOM)
        if self._music:
            self._screen.blit(self._images["music"], POS_MUSIC)
        if self._selected == 0:
            self._screen.blit(self._images["menu_marker"], SELECTED_POS_PLAY)
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
        text_left = ["Yay, you made it!",
                     "Next Level: " + str(info.index),
                     "Password: " + info.password,
                     "Press space to continue."]
        text_right = ["Score achieved: " + str(info.last_score),
                      "Time bonus: " + str(info.time_score),
                      "Total points: " + str(info.total_score)]
        self.draw_game_menu(info.index - 1, info.total_score, info.time_score)
        self.display_info(text_left, text_right)
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
        text_left = ["Awesome, well done!",
                     "You completed the game!",
                     "Please eat less animals.",
                     "Press space to continue."]
        text_right = ["Score achieved: " + str(info.last_score),
                      "Time bonus: " + str(info.time_score),
                      "Points for lives: " + str(info.bonus_score),
                      "Total points: " + str(info.total_score)]
        self.draw_game_menu(info.index, info.total_score, info.time_score)
        self.display_info(text_left, text_right)
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
        text_left = []
        text_right = []
        for score in sorted(highscores, reverse=True):
            text_left.append(str(score) + " - " + highscores[score][0])
            text_right.append("Level " + str(highscores[score][1]))
        self.set_game_menu(0)
        self.draw_game_menu(0, 0, 0)
        self.display_info(text_left, text_right)
        pg.display.flip()
        while True:
            self._clock.tick(FRAMERATE)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                    return

    def show_failure_screen(self, lives, info):
        """
        Shows a screen informing the user a level attempt has failed
        :param info: The game info object holding values for the game menu
        :param lives: number of lives the user has left
        :return: True if the user wants to and can continue playing, False otherwise
        """
        self._screen.fill(BACKGROUND_COLOR)
        text = ["Oh no, that did not work out."]
        if lives < 1:
            text.append("Sadly, you have no lives left.")
            text.append("Press space to return to the menu.")
        else:
            text.append("Lives left: " + str(lives))
            text.append("Press space to try again.")
        self.draw_game_menu(info.index, info.total_score, info.time_score)
        self.display_info(text, [])
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
        text_left = ["Enter the level password.",
                     "Leave empty for level 1.",
                     "Password:"]
        text_right = ["", "", password]
        self.set_game_menu(STARTING_LIVES)
        self.draw_game_menu(0, 0, 0)
        self.display_info(text_left, text_right)
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
            text_right[2] = password
            self.display_info(text_left, text_right)
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
        self.set_game_menu(0)
        self.draw_game_menu(0, 0, 0)
        self.display_info(text, [])
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
            self.display_info(text, [])
            pg.display.flip()

    def display_info(self, text_left, text_right):
        """
        Show text placed nicely on the placeholder image.
        A maximum of PLACEHOLDER_TEXT_MAX lines is shown
        :param text_right: list of text lines to display in the right section
        :param text_left: list of text lines to display in the left section
        :return: None
        """
        self._screen.blit(self._images["placeholder"], (0, 0))
        font = pg.font.Font(os.path.join(directories.GRAPHICS_DIRECTORY, "Minecraft.ttf"), PLACEHOLDER_TEXT_SIZE)
        for i in range(0, min(len(text_left), PLACEHOLDER_TEXT_MAX)):
            text_image = font.render(text_left[i], True, WHITE)
            text_rect = text_image.get_rect()
            text_rect.x = PLACEHOLDER_TEXT_X
            text_rect.y = PLACEHOLDER_TEXT_Y + i * PLACEHOLDER_TEXT_LINE_HEIGHT
            self._screen.blit(text_image, text_rect)
        for i in range(0, min(len(text_right), PLACEHOLDER_TEXT_MAX)):
            text_image = font.render(text_right[i], True, WHITE)
            text_rect = text_image.get_rect()
            text_rect.x = PLACEHOLDER_TEXT_X + PLACEHOLDER_TEXT_X_OFFSET
            text_rect.y = PLACEHOLDER_TEXT_Y + i * PLACEHOLDER_TEXT_LINE_HEIGHT
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
            digit = (number % (10 ** (length - i))) // (10 ** (length - i - 1))
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
