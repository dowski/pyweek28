# Stacky Tower
WIDTH = 600
HEIGHT = 800

BLOCK_BASIC = 'block_basic'

def make_block(block_type):
    return Actor(block_type)

def make_player():
    return {'tower': [], 'blocks': [], 'chosen_block': None}

player1 = make_player()
player2 = make_player()

def draw():
    screen.clear()
    for player in [player1, player2]:
        for block in player['tower']:
            block.draw()


def update():
    pass

def on_mouse_down(pos):
    add_block_to_tower(player1, BLOCK_BASIC)

def add_block_to_tower(player, block_type):
    block = make_block(block_type)
    block.y = HEIGHT - (len(player['tower']) * block.height + block.height / 2)
    block.x = WIDTH / 2
    player['tower'].append(block)