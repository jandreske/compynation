# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
# Directories for graphics, music and levels
DIRNAME = os.path.abspath(os.path.dirname(__file__))
LEVEL_DIRECTORY = os.path.join(DIRNAME, "levels")
GRAPHICS_DIRECTORY = os.path.join(DIRNAME, "graphics")
GENERAL_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "general")
MUSIC_DIRECTORY = os.path.join(DIRNAME, "music")
MENU_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "menu")
TILES_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "tiles")
NUMBERS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, "numbers")
