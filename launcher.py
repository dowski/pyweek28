"""
Mostly-working pyinstaller hack to get a PyGame zero executable
All data files included, and --onefile will compress everything down to ~15MB
Note that Pyinstaller moves everything to an internal directory, sys._MEIPASS,
and runs from that, so we have to explicitly use that path when loading the
game file.
Steps to (probably :*) ) replicate:
1. pip install pyinstaller
2. pyi-makespec --onefile alien.py
3. edit the alien.spec file, and change the datas part to:
             datas=[
                ('data', 'data'),
                ('images', 'images'),
                ('joystick_demo.py', '.')],
4. Copy your pgzero folder and data folder into your source directory.
    I have:
        - pgzero
        - data
        - images
        - joystick_demo.py (my original demo)
        - alien.py (this file)
        - alien.spec (the pyinstaller spec)
5. Comment out the body of the show_default_icon() function in
    pgzero/game.py:92-95 and add 'pass' to the end.
6. Run pyinstaller alien.spec
7. Your executable will be in the 'dist' folder.
Note that you'll need a gamepad/joystick with an analogue axis to play,
as well as the joystick_demo code
    <https://gist.github.com/AnthonyBriggs/f8b4d53cf9387e73fab5badb9cc06417>
and the two patches from my pygame zero repository that add mirroring and
joystick support.
"""

import os
import pygame
import sys
from types import ModuleType

from pgzero.runner import prepare_mod, run_mod


def main(path, repl=False):
    """Run a PygameZero module, with the path specified by the program.
    (Other than that, this is identical to the regular main() from runner.py)
    """
    with open(path) as f:
        src = f.read()

    print(os.path.basename(path))
    code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    sys.modules[name] = mod

    # Indicate that we're running with the pgzrun runner
    # This disables the 'import pgzrun' module
    sys._pgzrun = True

    prepare_mod(mod)
    exec(code, mod.__dict__)
    run_mod(mod)


# Need the full path if we're loading a file and compiling it
main(os.path.join(sys._MEIPASS, "stackytower.py"))