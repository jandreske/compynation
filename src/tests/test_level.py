import pytest
import numpy
import level

LEVEL_DIRECTORY = "../levels/"


def test_load():
    lvl = level.Level(LEVEL_DIRECTORY + "level_01")
    assert isinstance(lvl, level.Level)
    assert isinstance(lvl.field, numpy.ndarray)
    assert lvl.field.shape == (level.FIELD_Y, level.FIELD_X)


def test_missing_level():
    with pytest.raises(Exception):
        lvl = level.Level("does_not_exist")


def test_wrong_dimensions():
    with pytest.raises(Exception):
        lvl = level.Level("wrong_dimensions")
