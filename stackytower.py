# Stacky Tower
import random
import pygame.transform

WIDTH = 480
HEIGHT = 640

class Player:
    pass

player1 = Player()
player2 = Player()

# These are the x coordinates for the towers on the screen.
player1.towerx = WIDTH // 4
player2.towerx = player1.towerx * 3

# These values are used to know which direction the players are facing_left
# for drawing images and doing animations.
player1.facing_left = False
player2.facing_left = True

# In this game there are two players who race to build a tower of blocks.
# Each tower will be represented by a list created here. We can put blocks
# in the lists.
player1.tower = []
player2.tower = []

def make_inventory(towerx):
    """Makes a starting inventory to show on screen, centered on the towerx
    value."""
    inventory = [
        Actor('cannon_icon'), Actor('small_shield_icon'), Actor('basic')]
    inventory[1].pos = (towerx, 50)
    inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
    inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)
    return inventory

# These are the starting block inventories for both players. These blocks may
# be dropped onto their towers.
player1.inventory = make_inventory(player1.towerx)
player2.inventory = make_inventory(player2.towerx)

# These are the images of all available blocks.
icons = ['cannon_icon', 'small_shield_icon', 'basic', 'shotgun_icon']
full_block_map = {
    'cannon_icon': 'cannon',
    'small_shield_icon': 'small_shield',
    'basic': 'basic',
    'shotgun_icon': 'shotgun',
}

# This represents the currently selected block - it will be changed as
# the player changes block selection.
player1.selected_block = 1
player2.selected_block = 1

# This is used to indicate which block is selected on the screen.
selector1 = Actor('selected_block', (player1.towerx, 50))
selector2 = Actor('selected_block', (player2.towerx, 50))

# When player 1 drops a block, this variable will hold its Actor.
player1.falling_block = None
player2.falling_block = None

# Some debugging information - holds the duration that it took the last
# block to fall.
last_fall_duration = 0.0

# In the game, press / to show debug info
debug = False

def draw():
    screen.blit('background', (0, 0))
    draw_later = []
    for block in player1.tower:
        if block.image == 'small_shield':
            draw_later.append(block)
        else:
            block.draw()
    for block in player2.tower:
        if block.image == 'small_shield':
            draw_later.append(block)
        else:
            block.draw()
    # Now that the two towers have most of their blocks drawn,
    # we can draw the small shields which have to be drawn on
    # top of other blocks.
    for block in draw_later:
        block.draw()
    for block in player1.inventory:
        block.draw()
    for block in player2.inventory:
        block.draw()
    if player1.falling_block:
        player1.falling_block.draw()
    if player2.falling_block:
        player2.falling_block.draw()
    if debug:
        screen.draw.text("last_fall_duration: {}".format(
            last_fall_duration), (10, 80))
    selector1.draw()
    selector2.draw()

def replace_block(player):
    """Replaces the previously selected block with a new random block."""
    new_block_image = random.choice(icons)
    new_block = Actor(new_block_image)
    new_block.x = player.towerx
    new_block.y = 50
    player.inventory[player.selected_block] = new_block

def drop_block(player):
    """Animates the dropping action of the selected block."""
    global last_fall_duration
    block = player.inventory[player.selected_block]
    block.x = player.towerx
    block.image = full_block_map[block.image]
    if player.facing_left:
        flip_actor_image(block)
    block.target_y = HEIGHT - len(player.tower) * 32 - 32 // 2
    last_fall_duration = duration = 1.0 * (block.target_y / HEIGHT)
    animate(block, duration=duration, y=block.target_y, tween='bounce_end',
            on_finished=stop_dropping)
    player.falling_block = block

def stop_dropping():
    """Adds the block that just fell to the tower."""
    if player1.falling_block and (
            player1.falling_block.y == player1.falling_block.target_y):
        player1.tower.append(player1.falling_block)
        player1.falling_block = None
    if player2.falling_block and (
            player2.falling_block.y == player2.falling_block.target_y):
        player2.tower.append(player2.falling_block)
        player2.falling_block = None

def on_key_up(key):
    # When the S key is pressed, add a block for player 1
    global debug
    if key == keys.S and not player1.falling_block:
        drop_block(player1)
        replace_block(player1)
        print("Player 1 tower has {} blocks".format(len(player1.tower)))
    # When the K key is pressed, add a block for player 2
    elif key == keys.K and not player2.falling_block:
        drop_block(player2)
        replace_block(player2)
        print("Player 2 tower has {} blocks".format(len(player2.tower)))

    elif key == keys.A and player1.selected_block < 2:
        # Move player1 selected block left
        switch_selected_block(player1, -1)
    elif key == keys.D and player1.selected_block > 0:
        # Move player1 selected block right
        switch_selected_block(player1, 1)

    elif key == keys.J and player2.selected_block < 2:
        # Move player2 selected block left
        switch_selected_block(player2, -1)
    elif key == keys.L and player2.selected_block > 0:
        # Move player1 selected block right
        switch_selected_block(player2, 1)

    elif key == keys.SLASH:
        debug = not debug

def switch_selected_block(player, direction):
    """Given a direction of either 1 or -1, changes the selected block."""
    player.inventory[1].pos = (
        player.inventory[1].x + (direction * player.inventory[1].width),
        player.inventory[1].y)
    player.inventory[0].pos = (
        player.inventory[0].x + (direction * player.inventory[0].width),
        player.inventory[0].y)
    player.inventory[2].pos = (
        player.inventory[2].x + (direction * player.inventory[2].width),
        player.inventory[2].y)
    player.selected_block -= direction

def flip_actor_image(actor):
    actor._surf = pygame.transform.flip(actor._orig_surf, True, False)