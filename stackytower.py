import random
# Stacky Tower

WIDTH = 480
HEIGHT = 640

# In this game there are two players who race to build a tower of blocks.
# Each tower will be represented by a list created here. We can put blocks
# in the lists.
tower1 = []
tower2 = []
cannon = Actor('cannon')
small_shield = Actor('small_shield')
basic = Actor('basic')
inventory = [cannon, small_shield, basic]
picture = ['cannon', 'small_shield', 'basic', 'shotgun', 'large_shield']
all_blocks = [cannon, small_shield, basic]
selected_block = 1
new_block = 0
TOWER1_X = WIDTH // 4
TOWER2_X = TOWER1_X * 3
inventory[1].pos = (TOWER1_X, 50)
inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)

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
    if debug:
        screen.draw.text("inventory: {}".format(", ".join(i.image for i in inventory)), (10, 80))
        screen.draw.text("selected_block: {}".format(selected_block), (10, 100))


def update():
    pass

def replace_block():
    new_block_image = random.choice(picture)
    new_block = Actor(new_block_image)
    new_block.x = TOWER1_X
    new_block.y = 50
    inventory[selected_block] = new_block


def on_key_up(key):
    # When the S key is pressed, add a block for player 1
    global selected_block, debug
    if key == keys.S:
        block = inventory[selected_block]
        block.x = TOWER1_X
        block.y = HEIGHT - len(tower1) * block.height - block.height // 2
        tower1.append(block)
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
    global selected_block
    inventory[1].pos = (inventory[1].x + (direction * inventory[1].width), inventory[1].y)
    inventory[0].pos = (inventory[0].x + (direction * inventory[0].width), inventory[0].y)
    inventory[2].pos = (inventory[2].x + (direction * inventory[2].width), inventory[2].y)
    selected_block -= direction