# File for constants used for the game and display
STARTING_LIVES = 3
SONGS = ["adventure.mp3", "arcade.mp3", "boss.mp3", "castle.mp3", "funny.mp3"]
# Game size values
BLOCK_SIZE = 64
MENU_BLOCK_WIDTH = 4
FIELD_X = 14
FIELD_Y = 10
# Info box values
NUMBER_WIDTH = 34
TIME_X = FIELD_X * BLOCK_SIZE + 100
TIME_Y = 110
SCORE_X = FIELD_X * BLOCK_SIZE + 65
SCORE_Y = 315
LEVEL_X = FIELD_X * BLOCK_SIZE + 100
LEVEL_Y = 475
# Placeholder image values
PLACEHOLDER_TEXT_X = 220
PLACEHOLDER_TEXT_X_OFFSET = 270
PLACEHOLDER_TEXT_Y = 275
PLACEHOLDER_TEXT_MAX = 5
PLACEHOLDER_TEXT_LINE_HEIGHT = 42
PLACEHOLDER_TEXT_SIZE = 20
# Main menu positions
POS_LIVES = (FIELD_X * BLOCK_SIZE, 372)
POS_TIME = (FIELD_X * BLOCK_SIZE, 403)
POS_RANDOM = (FIELD_X * BLOCK_SIZE, 435)
POS_MUSIC = (FIELD_X * BLOCK_SIZE, 472)
# Tile image values
MOVE_MIN_TILE = 1
MOVE_MAX_TILE = 15
BACK_DEFAULT_TILE = 100
BACK_MIN_TILE = 100
BACK_MAX_TILE = 117
DEFAULT_BACKGROUND_PERCENTAGE = 0.7
# Dictionary for menu entries
MENU_ENTRIES = {0: "play", 1: "info", 2: "password", 3: "lives", 4: "time", 5: "music", 6: "random", 7: "highscores"}
# User interaction values
FRAMERATE = 60
STABILIZING_FRAMERATE = 4
# Colors
BACKGROUND_COLOR = (0x15, 0x0D, 0x09)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
