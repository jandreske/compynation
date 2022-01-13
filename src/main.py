import math
from level import Level, FIELD_X, FIELD_Y
import pygame as pg
import os
from level_info import LevelInfo
from ui_manager import UI
import directories

STARTING_LIVES = 3


def main():
    """
    Main entry point into the game, this function initializes everything and then runs the main menu loop
    :return: None
    """
    ui = UI()
    ui.draw_menu()
    running = True
    while running:
        ui.clock.tick(60)
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
                    elif choice == "random":
                        ui.flip_random()
                    elif choice == "highscores":
                        ui.show_highscores(load_highscores())
                    elif choice == "play":
                        play_game(ui)
                ui.draw_menu()


def play_game(ui):
    """
    Organizes the sequence of levels to play. Loads the level info from a file, allows user password input
    and manages info screens in between solved or failed levels
    :param ui: The ui instance managing the interface
    :return: None
    """
    info = LevelInfo(os.path.join(directories.LEVEL_DIRECTORY, "list"))
    password = ui.show_password_screen()
    level = load_level(info.by_password(password))
    lives = STARTING_LIVES
    score = 0
    playing = True
    while playing:
        if play_level(ui, level):
            score = score + level.score
            next_level = info.next
            if not next_level:
                bonus = 0
                if ui.lives:
                    bonus = lives * 2 * math.floor(score / info.last)
                score = score + bonus
                ui.show_winning_screen(level.score, bonus, score)
                playing = False
            else:
                if ui.show_success_screen(info, level.score, score):
                    level = load_level(next_level)
                else:
                    playing = False
        else:
            if ui.lives:
                lives = lives - 1
            playing = ui.show_failure_screen(lives)
    check_highscores(ui, score)


def play_level(ui, level):
    """
    Loads a level and then runs the loop to play the game, allowing the user to make moves.
    :param ui: the ui instance used for managing the interface
    :param level: the level object containing the initial game state
    :return: True if the level was cleared, False otherwise
    """
    if ui.random:
        level.randomize(1, 7, 100, 106, 100)
    ui.draw(level)
    position = (0, 0)
    ui.draw_marker(position)
    pg.display.flip()
    while True:
        ui.clock.tick(60)
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
            ui.draw(level)
            ui.draw_marker(position)
            pg.display.flip()
            while not level.stable:
                ui.clock.tick(4)
                level.stabilize()
                ui.draw(level)
                ui.draw_marker(position)
                pg.display.flip()
            if level.solved:
                return True


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
