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
picture = ['cannon', 'small_shield', 'basic']
all_blocks = [cannon, small_shield, basic]
selected_block = 1
new_block = 0
TOWER1_X = WIDTH // 4
TOWER2_X = TOWER1_X * 3
inventory[1].pos = (TOWER1_X, 50)
inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)

def draw():
    screen.clear()
    for block in tower1:
        block.draw()
    for block in tower2:
        block.draw()
    for block in inventory:
        block.draw()



def update():
    pass

def replace_block():
    new_block_image = random.choice(picture)
    new_block = Actor(new_block_image)
    new_block.x = TOWER1_X
    new_block.y = 50
    inventory[selected_block] = new_block


def on_key_down(key):
    # When the S key is pressed, add a block for player 1
    global selected_block
    if key == keys.S:
        block = inventory[selected_block] = Actor(picture[selected_block])
        block.x = TOWER1_X
        block.y = HEIGHT - block.height // 2
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
def on_key_up(key):
    global selected_block
    if key == keys.A:
        if selected_block > 0:
            inventory[1].pos = (inventory[1].x - 32, 50)
            inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
            inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)
            selected_block -= 1
    if key == keys.D:
        if selected_block < 2:
            inventory[1].pos = (inventory[1].x + 32, 50)
            inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
            inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)
            selected_block += 1