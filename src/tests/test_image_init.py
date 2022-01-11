import pytest
import ui_manager

IMAGES = ["info", "logo", "welcome", "game_marker", "menu_marker"]


def test_load():
    ui = ui_manager.UI()
    assert len(ui._images) == len(IMAGES)
    for img in IMAGES:
        assert img in ui._images.keys()
    with pytest.raises(KeyError):
        var = ui._images["does_not_exist"]
    assert len(ui._menu_pics) == len(ui_manager.MENU_ENTRIES)
    for img in ui_manager.MENU_ENTRIES.keys():
        assert img in ui._menu_pics.keys()
    with pytest.raises(KeyError):
        var = ui._menu_pics[1077]
    assert len(ui._tile_dict) == 14
    for tile in range(100, 107):
        assert tile in ui._tile_dict.keys()
    for tile in range(1, 8):
        assert tile in ui._tile_dict.keys()
    with pytest.raises(KeyError):
        var = ui._tile_dict[2317]
