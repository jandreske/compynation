import pytest
import main


def test_load_save():
    scores = main.load_highscores()
    main.save_highscores(scores)
