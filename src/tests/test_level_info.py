import pytest
import level_info

LEVEL_DIRECTORY = "../levels/"


def test_load():
    info = level_info.LevelInfo(LEVEL_DIRECTORY + "list.txt")
    assert isinstance(info, level_info.LevelInfo)
    assert isinstance(info._byPassword, dict)
    assert isinstance(info._passwords, dict)
    assert isinstance(info._byIndex, dict)


def test_exceptions():
    info = level_info.LevelInfo(LEVEL_DIRECTORY + "list.txt")
    with pytest.raises(Exception):
        val = info.next
    with pytest.raises(Exception):
        val = info.password
    val = info.first
    with pytest.raises(Exception):
        val = info.first
    with pytest.raises(Exception):
        val = info.by_password("")


def test_sequence():
    info = level_info.LevelInfo(LEVEL_DIRECTORY + "list.txt")
    level = info.first
    assert level == "level_01"
    assert info.index == 1
    assert info.password == ""
    level = info.next
    assert level == "level_02"
    assert info.index == 2
    assert info.password == "BACARDI"
    level = info.next
    assert level == "level_03"
    assert info.index == 3
    assert info.password == "CAXXON"
