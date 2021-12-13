# Original C64 Combination

### Splash screen
* Music
* Animated text banners
* Copyright 1994 by Magic Disk
* Author contact info and greetings
* Credits (code, graphics, music)

### Launch menu
* Infinite Lives (Y/N)? -> always 2 lives left
* Infinite Time (Y/N)? -> does not tick down, always full time bonus
* Levelskip (Y/N)? -> not yet clear
* Wanna see THE END (Y/N)? -> shows end screen instead of starting game
* Passwords for levels 02 to 40

### Welcome screen
* Game banner (animated)
* Game music
* Highscores
* Some keys explained (space in menu vs ingame)
* Credits and Thanks

### Password entry
* Enter password to start in higher level
* Empty password starts at 1

### Game play
* Time available: depends on level. Seconds: 25 - 25 - 30 - 30 - 30 - 30 - 38 - 55 - 55 - 28
* Score: Time bonus (1 point per second?) and number of blocks eliminated 2:20, 3:40
* Move "target" frame (up, down, left, right)
* Hold fire button while moving to move "selected" block along (if movable and only left / right)
* After each step, game state settles: blocks fall down, after that touching identical blocks disappear, repeats until stable
* Touching blocks increase score
* Time ticks down
* No movable blocks left: level cleared
* No time left or space bar pressed: level failed

### Level failed
* Tough luck message (+ you seemed to have difficulties...)
* Shows number of lives left
* Press button to try again

### Level cleared
* Congratulations message and overall rating ("below average")
* Score breakdown (old score, time bonus, new score)
* Password for next level
* Press button for next level

### Game Over
* Result (score and level)
* Enter name for highscore

### End screen
* "You did it" scrolling text
* Credits


