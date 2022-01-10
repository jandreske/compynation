import pytest
import main

IMAGES = ["info", "logo", "welcome", "game_marker", "menu_marker"]


def test_load():
    assert len(main.IMAGES) == 0
    assert len(main.MENU_PICS) == 0
    assert len(main.TILE_DICT) == 0
    main.load_images()
    assert len(main.IMAGES) == len(IMAGES)
    for img in IMAGES:
        assert img in main.IMAGES.keys()
    with pytest.raises(KeyError):
        var = main.IMAGES["does_not_exist"]
    assert len(main.MENU_PICS) == len(main.MENU_ENTRIES)
    for img in main.MENU_ENTRIES.keys():
        assert img in main.MENU_PICS.keys()
    with pytest.raises(KeyError):
        var = main.MENU_PICS[1077]
    assert len(main.TILE_DICT) == 7
    for tile in range(100, 107):
        assert tile in main.TILE_DICT.keys()
    with pytest.raises(KeyError):
        var = main.TILE_DICT[2317]
