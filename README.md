# Stacky Tower

## Overview
Stacky Tower is an [entry for PyWeek 28](https://pyweek.org/e/rohirrim/).

![screenshot](https://pyweek.org/media/dl/28/rohirrim/Pygame_Zero_Game_9_28_2019_2_22_32_PM.png)

It's a turn based game where you race another player to build the tallest tower.

Along the way you can damage your opponent's tower, put up shields and repair your tower if it's damaged.

Be smart about which blocks you play when! It might be the difference between a win and a loss!

## Playing

The game may be played from source or by using a pre-built Windows executable.

The easiest way to play from source is to use the [Mu editor](https://codewith.mu/). Check out the Stacky Tower code
from this repo (or extract a zip file) to your preferred location and open `stackytower.py` in Mu. Choose PyGame Zero
from the Mode selection button and then click Play.

You can also simply extract the .zip file into a virtualenv, `pip install pgzero==1.2` and run `pgzrun stackytower.py`.

If you are running on a Windows platform you may opt to use a pre-built executable (`stackytower.exe`).

### Game Play

The game opens to a menu. Follow the basic instructions for play within the game.

### Custom Keyboard Layouts

If you use a non-QWERTY keyboard layout you'll need to play from source. You can edit the key mapping at the top of
`stackytower.py` to suit your preferences.

## Credits

This game was designed and coded by Christian Wyglendowski and Eli Wyglendowski.

Most graphics were created by Eli.

It uses the [PyGame Zero](https://pygame-zero.readthedocs.io/en/stable/) game framework, some graphics by
[Kenney](https://kenney.nl), sound effects created with [sfxr](http://www.drpetter.se/project_sfxr.html) and the
[1980xx font by Vold](https://arcade.itch.io/1980). MS Paint and Paint 3D were also used for creating graphics.

The app was largely coded using the [Mu editor](https://codewith.mu/) and runs on [Python 3](https://www.python.org).

The EXE version was built with [Pyinstaller](https://www.pyinstaller.org/) and uses a modified PyGame Zero
[launcher recipe](https://gist.github.com/AnthonyBriggs/cac72989c2dd3c4aeb7475237079d2fb) by AnthonyBriggs.

## License
The code is released under the MIT license.