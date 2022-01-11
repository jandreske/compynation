from level import Level, FIELD_X, FIELD_Y
import pygame as pg
import os
from level_info import LevelInfo
from ui_manager import UI
import directories


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
                    elif choice == "random":
                        ui.flip_random()
                    elif choice == "play":
                        play_game(ui)
                ui.draw_menu()


def load_level(name):
    """
    Loads a level from a file
    :param name: the name of the level file in the levels directory
    :return: The Level object constructed from the file content
    """
    return Level(os.path.join(directories.LEVEL_DIRECTORY, name))


def play_game(ui):
    """
    Organizes the sequence of levels to play. Loads the level info from a file, allows user password input
    and manages info screens in between solved or failed levels
    :param ui: The ui instance managing the interface
    :return: None
    """
    info = LevelInfo(os.path.join(directories.LEVEL_DIRECTORY, "list.txt"))
    password = ui.show_password_screen()
    level = load_level(info.by_password(password))
    playing = True
    while playing:
        if play_level(ui, level):
            next_level = info.next
            if not next_level:
                # winning screen
                playing = False
            else:
                if ui.show_success_screen(info):
                    level = load_level(next_level)
                else:
                    playing = False
        else:
            # Leben checken, fragen ob weiter spielen?
            playing = False
    # punkte anzeigen etc, highscore


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


if __name__ == "__main__":
    main()
