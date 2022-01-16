import random
import main


def test_load_save():
    scores = main.load_highscores()
    assert len(scores.keys()) == 5
    assert len(random.choice(list(scores.items()))) == 2
    main.save_highscores(scores)
