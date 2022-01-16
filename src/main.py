import math
import random
import time
from level import Level
from level_info import LevelInfo
from ui_manager import *
import directories
from game_constants import *


def main():
    """
    Main entry point into the game, this function initializes everything and then runs the main menu loop
    :return: None
    """
    ui = UI()
    ui.draw_menu()
    start_menu_music()
    running = True
    while running:
        ui.clock.tick(FRAMERATE)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    ui.menu_up()
                elif event.key == pg.K_DOWN:
                    ui.menu_down()
                elif event.key == pg.K_SPACE:
                    choice = ui.selected
                    if choice == "quit":
                        running = False
                    elif choice == "info":
                        ui.flip_info()
                    elif choice == "lives":
                        ui.flip_lives()
                    elif choice == "time":
                        ui.flip_time()
                    elif choice == "music":
                        ui.flip_music()
                        if ui.music:
                            start_menu_music()
                        else:
                            stop_music()
                    elif choice == "random":
                        ui.flip_random()
                    elif choice == "highscores":
                        ui.show_highscores(load_highscores())
                    elif choice == "play":
                        play_game(ui, False)
                    elif choice == "password":
                        play_game(ui, True)
                ui.draw_menu()


def start_menu_music():
    """
    Loads the menu music and starts playing it
    :return: None
    """
    pg.mixer.music.load(os.path.join(directories.MUSIC_DIRECTORY, "menu.mp3"))
    pg.mixer.music.play(-1)


def start_level_music():
    """
    Loads a random song from the list of level songs and plays it
    :return: None
    """
    song = random.choice(SONGS)
    pg.mixer.music.load(os.path.join(directories.MUSIC_DIRECTORY, song))
    pg.mixer.music.play(-1)


def stop_music():
    """
    Stops the background music playback
    :return: None
    """
    pg.mixer.music.stop()


def play_game(ui, pw_entry):
    """
    Organizes the sequence of levels to play. Loads the level info from a file, allows user password input
    and manages info screens in between solved or failed levels
    :param pw_entry: whether the user should be asked for a password
    :param ui: The ui instance managing the interface
    :return: None
    """
    stop_music()
    info = LevelInfo(os.path.join(directories.LEVEL_DIRECTORY, "list"))
    if pw_entry:
        password = ui.show_password_screen()
        info.by_password(password)
    else:
        info.first()
    lives = STARTING_LIVES
    ui.set_game_menu(lives)
    playing = True
    while playing:
        if ui.music:
            start_level_music()
        success = play_level(ui, info)
        stop_music()
        if success:
            next_level = info.next
            if not next_level:
                if ui.lives:
                    info.set_bonus(lives)
                ui.show_winning_screen(info)
                playing = False
            else:
                if not ui.show_success_screen(info):
                    playing = False
        else:
            if ui.lives:
                lives = lives - 1
                ui.set_game_menu(lives)
            playing = ui.show_failure_screen(lives, info)
    if ui.music:
        start_menu_music()
    check_highscores(ui, info.total_score)


def play_level(ui, info):
    """
    Loads a level and then runs the loop to play the game, allowing the user to make moves.
    :param info: the level info object tracking scores
    :param ui: the ui instance used for managing the interface
    :return: True if the level was cleared, False otherwise
    """
    level = load_level(info.current)
    if ui.random:
        level.randomize(MOVE_MIN_TILE, MOVE_MAX_TILE, BACK_MIN_TILE, BACK_MAX_TILE, BACK_DEFAULT_TILE)
    position = (0, 0)
    time_left = 0
    if ui.time:
        time_left = info.time
    ui.draw(level)
    ui.draw_marker(position)
    ui.draw_game_menu(info.index, info.total_score + level.score, time_left)
    pg.display.flip()
    start = time.time()
    while True:
        ui.clock.tick(FRAMERATE)
        new_position = position
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if ui.lives:
                    info.set_scores(level.score, time_left)
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if ui.lives:
                        info.set_scores(level.score, time_left)
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
            ui.draw(level)
            ui.draw_marker(position)
            ui.draw_game_menu(info.index, info.total_score + level.score, time_left)
            pg.display.flip()
            while not level.stable:
                # way lower framerate to make movements visible
                ui.clock.tick(STABILIZING_FRAMERATE)
                level.stabilize()
                ui.draw(level)
                ui.draw_marker(position)
                ui.draw_game_menu(info.index, info.total_score + level.score, time_left)
                pg.display.flip()
            if level.solved:
                info.set_scores(level.score, time_left)
                return True
        new_time_left = info.time - math.floor(time.time() - start)
        if ui.time and new_time_left < time_left:
            time_left = new_time_left
            ui.draw_game_menu(info.index, info.total_score + level.score, time_left)
            pg.display.flip()
        if ui.time and time_left < 0:
            return False


def check_highscores(ui, score):
    """
    Vhecks whether the score is a new highscore, adds it if so and shows the highscores after
    :param ui: UI manager to display highhscores
    :param score: score achieved by the user
    :return: None
    """
    highscores = load_highscores()
    if len(highscores) < 5 or score > min(highscores.keys()):
        name = ui.get_user_name()
        highscores[score] = name
        if len(highscores) > 5:
            del highscores[min(highscores.keys())]
        save_highscores(highscores)
    ui.show_highscores(highscores)


def load_highscores():
    """
    Loads the highscores from a file into a dictionary
    :return: The dictionary containing highscore values
    """
    scores = {}
    with open(os.path.join(directories.LEVEL_DIRECTORY, "highscores"), "r") as file:
        for line in file.readlines():
            if line == "":
                continue
            values = line.strip().split(',')
            if len(values) != 2:
                raise Exception("Highscore file broken, invalid number of fields.")
            try:
                scores[int(values[0])] = values[1]
            except Exception:
                raise Exception("Highscore file broken, invalid line.")
    return scores


def save_highscores(highscores):
    """
    Saves the highscores from a dict to a file
    :param highscores: the dictionary containing the highscores
    :return: None
    """
    with open(os.path.join(directories.LEVEL_DIRECTORY, "highscores"), "w") as file:
        for score in highscores.keys():
            file.write(str(score) + "," + highscores[score] + "\n")


def load_level(name):
    """
    Loads a level from a file
    :param name: the name of the level file in the levels directory
    :return: The Level object constructed from the file content
    """
    return Level(os.path.join(directories.LEVEL_DIRECTORY, name))


if __name__ == "__main__":
    main()
