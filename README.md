# Compynation
This project is a python clone of the C64 game combination.
It was created by Jan Dreske as part of the coding competition of the VU informatics course at the bachelor of astronomy studies at University of Vienna.

### Requirements
Python 3 and pip are required to run the game and setup.  
Additional modules are necessary and can be installed using the setup.sh script.

### Setup and run
After unpacking the archive, execute  

    ./setup.sh
in order to install required python modules.  
Then run  

    ./start.sh
to start the game.

### Game mechanics
The objective of the game is to connect matching gems, making them disappear and clearing the level.
In the main menu, use the enter key to show the game info. User arrow keys to navigate the menu and space to select an entry.  
In the game, use arrow keys to move the marker and hold space while doing so to move a gem. Clear the level by removing all gems.

### In this package
- README: this text here
- LICENSE: a copy of the MPL 2 license this game is distributed under
- run_tests.sh: a bash script to execute the tests
- setup.sh: a bash script to install required modules
- start.sh: a bash script to start the game
- tests: a directory containing the tests for the code
- doc: a directory containing the project plan, architecture outline and documentation of combination
- src: the sources directory, containing the python code
  * graphics: contains all images for the game and the font
  * levels: contains the level data, overview and highscore list
  * music: the music files used for background music

### Thanks
Many thanks to **The Creators** for the original C64 game.  
Thanks to **Craftron Gaming** for providing the free and open Minecraft font.  
Thanks to **Fesliyan Studios** for providing the music for this game.  
Thanks to the **PyGame Community** for providing the gaming framework.  

Many many special thanks to **ashyda** for all the game graphics.  
Without you, this would have worked fine but looked awful.  

Thanks to **Lisa** for always encouraging me, providing snacks and playtesting the game.
