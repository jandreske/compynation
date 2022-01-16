import pytest
import numpy
import level

LEVEL_DIRECTORY = "../src/levels/"


def test_load():
    lvl = level.Level(LEVEL_DIRECTORY + "level_01")
    assert isinstance(lvl, level.Level)
    assert isinstance(lvl.field, numpy.ndarray)
    assert lvl.field.shape == (level.FIELD_Y, level.FIELD_X)


def test_missing_level():
    with pytest.raises(Exception):
        level.Level("does_not_exist")


def test_wrong_dimensions():
    with pytest.raises(Exception):
        level.Level("wrong_dimensions")


def test_move():
    lvl = level.Level(LEVEL_DIRECTORY + "level_01")
    before_right = lvl.field[4][6]
    before_left = lvl.field[4][5]
    assert not lvl.move((0, 0), -1)
    assert not lvl.move((6, 4), -2)
    assert not lvl.move((6, 4), 1)
    assert lvl.move((6, 4), -1)
    after_right = lvl.field[4][6]
    after_left = lvl.field[4][5]
    assert before_right == after_left
    assert before_left == after_right


def test_stabilize():
    lvl = level.Level(LEVEL_DIRECTORY + "level_01")
    lvl.move((6, 5), -1)
    assert not lvl.stable
    assert not lvl.move((7, 4), -1)
    assert not lvl.stabilize()
    assert not lvl.stable
    assert not lvl.move((7, 4), -1)
    assert lvl.stabilize()
    assert lvl.stable
    assert lvl.move((7, 4), -1)
    assert not lvl.stable
    assert lvl.stabilize()
    assert lvl.stable
