# Stacky Tower
import random

WIDTH = 480
HEIGHT = 640

# These are the x coordinates for the towers on the screen.
TOWER1_X = WIDTH // 4
TOWER2_X = TOWER1_X * 3

# In this game there are two players who race to build a tower of blocks.
# Each tower will be represented by a list created here. We can put blocks
# in the lists.
tower1 = []
tower2 = []
cannon = Actor('cannon')
small_shield = Actor('small_shield')
basic = Actor('basic')

# This is the starting block inventory for the player. These blocks may
# be dropped onto the tower.
inventory = [cannon, small_shield, basic]
inventory[1].pos = (TOWER1_X, 50)
inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)

# These are the images of all available blocks.
picture = ['cannon', 'small_shield', 'basic', 'shotgun', 'large_shield']

# This represents the currently selected block - it will be changed as
# the player changes block selection.
selected_block = 1

# This is used to indicate which block is selected on the screen.
selected = Actor('selected_block', (TOWER1_X, 50))

# When player 1 drops a block, this variable will hold its Actor.
player1_falling_block = None

# Some debugging information - holds the duration that it took the last
# block to fall.
last_fall_duration = 0.0

# In the game, press / to show debug info
debug = False

def draw():
    screen.clear()
    for block in tower1:
        block.draw()
    for block in tower2:
        block.draw()
    for block in inventory:
        block.draw()
    if player1_falling_block:
        player1_falling_block.draw()
    if debug:
        screen.draw.text("inventory: {}".format(
            ", ".join(i.image for i in inventory)), (10, 80))
        screen.draw.text("selected_block: {}".format(
            selected_block), (10, 100))
        screen.draw.text("last_fall_duration: {}".format(
            last_fall_duration), (10, 120))
    selected.draw()


def update():
    pass

def replace_block():
    """Replaces the previously selected block with a new random block."""
    new_block_image = random.choice(picture)
    new_block = Actor(new_block_image)
    new_block.x = TOWER1_X
    new_block.y = 50
    inventory[selected_block] = new_block

def drop_block():
    """Animates the dropping action of the selected block."""
    global player1_falling_block, last_fall_duration
    block = inventory[selected_block]
    block.x = TOWER1_X
    target_y = HEIGHT - len(tower1) * block.height - block.height // 2
    last_fall_duration = duration = 1.0 * (target_y / HEIGHT)
    animate(block, duration=duration, y=target_y, tween='bounce_end',
            on_finished=stop_dropping)
    player1_falling_block = block

def stop_dropping():
    """Adds the block that just fell to the tower."""
    global player1_falling_block
    tower1.append(player1_falling_block)
    player1_falling_block = None

def on_key_up(key):
    # When the S key is pressed, add a block for player 1
    global selected_block, debug
    if key == keys.S and not player1_falling_block:
        drop_block()
        replace_block()
        print("Player 1 tower has {} blocks".format(len(tower1)))
    # When the K key is pressed, add a block for player 2
    elif key == keys.K:
        block = Actor('block_basic')
        block.x = TOWER2_X
        block.y = HEIGHT - block.height // 2
        tower2.append(block)
        print("Player 2 tower has {} blocks".format(len(tower2)))
    elif key == keys.SLASH:
        debug = not debug

    if key == keys.A:
        if selected_block < 2:
            switch_selected_block(-1)
    if key == keys.D:
        if selected_block > 0:
            switch_selected_block(1)

def switch_selected_block(direction):
    """Given a direction of either 1 or -1, changes the selected block."""
    global selected_block
    inventory[1].pos = (
        inventory[1].x + (direction * inventory[1].width), inventory[1].y)
    inventory[0].pos = (
        inventory[0].x + (direction * inventory[0].width), inventory[0].y)
    inventory[2].pos = (
        inventory[2].x + (direction * inventory[2].width), inventory[2].y)
    selected_block -= direction