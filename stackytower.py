# Stacky Tower
WIDTH = 480
HEIGHT = 640

# In this game there are two players who race to build a tower of blocks.
# Each tower will be represented by a list created here. We can put blocks
# in the lists.
tower1 = []
tower2 = []

# This bit of math gives us X values to evenly places the towers on the screen.
TOWER1_X = WIDTH // 4
TOWER2_X = TOWER1_X * 3

def draw():
    screen.clear()
    for block in tower1:
        block.draw()
    for block in tower2:
        block.draw()

def update():
    pass

def on_key_down(key):
    # When the S key is pressed, add a block for player 1
    if key == keys.S:
        block = Actor('block_basic')
        block.x = TOWER1_X
        block.y = HEIGHT - block.height // 2
        tower1.append(block)
        print("Player 1 tower has {} blocks".format(len(tower1)))
    # When the K key is pressed, add a block for player 2
    elif key == keys.K:
        block = Actor('block_basic')
        block.x = TOWER2_X
        block.y = HEIGHT - block.height // 2
        tower2.append(block)
        print("Player 2 tower has {} blocks".format(len(tower2)))