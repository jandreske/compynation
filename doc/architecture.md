# Architecture draft

For a diagram, see the [architecture plan](architecture_plan.png)  
The plan is to keep - if possible - all functional parts of the original game.  
Some of those will be made optional extensions, though:  
- limited lives
- time limits
- highscores
- music

That way, I can focus on a working base structure first and then add these parts later.  
This is not to say they are not relevant or outside of the scope, but not strictly necessary to get a minimumal version done.  

### Components

#### Menu
I will have single View that acts as a Menu and also Splash Screen and Credits overview.  
That seems easier to do and I do not need to figure out how to distribute (and potentially replicate) information.  
This part is definitely necessary for the core functionality to feel complete, but various parts and options can be added over time.

#### Level loading
At this point I assume I will store levels as text in files and load them as required.  
That way, levels can separately be edited and added and also potentially generated with other software later.  
Level loading is also part of the base functionality, as it is required to play at all.

#### Passwords
Being able to enter passwords to skip to a specific level is also considered a base game component by me.  
The actual components might be added late among the base stuff though, since it seems this is less crucial than actually playing the game.  
I might store a mapping list as a file along with the levels, containing the passwords and corresponding level files and numbers.  
With the source of the game available there is no point in trying to hide the passwords anyway, and that way level management might be more flexible.

#### Playing
So this might be one component or two, depending on how intertwined or separate the game logic and the UI will be.  
The backend part is basically running stuff in a loop.
- make a move (so user input, check if valid, move piece)
- repeat these two until nothing moves anymore:
  - let blocks fall down until everything is on the ground
  - disappear matching connecting blocks (and up the score accordingly)
  - In between the steps the UI needs updating, probably after each "tick" of anything moving or disappearing.
- Check whether the game is won or lost
Definitely a base component, basically the heart of it all.  
Seems like game mechanics / business logic will be fine, UI will be the hard / interesting part to do.

#### Limited lives
Optional addon.  
Would be nice to have for sure, but should only be tackled once the base game is working.  
Basically just a counter countin failures und not allowing retries any more once lives ran out.  
Option in the menu to give endless lives might came together with this one.

#### Time limits
Also optional, thus being done later if time permits.  
Basically just a timer starting with each level, and if it runs out, the level fails.  
Gives extra points for cleared levels based on the time left.  
Also needs to be stored somewhere. Maybe in the same lookup file with level passwords?

#### Highscores
Optional addon.  
For the base game, I will just skip back to the menu after lives did run out or the player leaves.  
With this, I will save high scores somewhere (guess a flat text file?) and let people enter their names.  
Scores will then get sorted into the list and shown after playing, plus an option to switch between menu and highscore list.

#### Music
Yeah, once everything works I can check whether I can play background music.  
During the levels and maybe also in the menu.  
Need to acquire some copyright-free music for that and add a menu option to switch it off.

#### Nice graphics
Like, having _anything_ at all is necessary for the base game.  
But having something nicer to look at - that can be updated later.  
I will aim to make the block images and so on easy to replace later.  
Might ask a friend to whip up some stuff for me.
