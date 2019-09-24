# Stacky Tower
WIDTH = 600
HEIGHT = 800

HALF_WIDTH = WIDTH // 2
PLAYER_1_X = HALF_WIDTH - HALF_WIDTH // 2
PLAYER_2_X = HALF_WIDTH + HALF_WIDTH // 2

INVENTORY_MIDDLE = 1

BLOCK_BASIC = 'block_basic'


def add_block(block_type, player):
    block = Actor(block_type)
    block.y = block.height // 2
    if len(player['inventory']) < 3:
        block.x = player['x'] + len(player['inventory']) * block.width - block.width
        player['inventory'].append(block)
    else:
        block.x = player['x']
        player['inventory'][INVENTORY_MIDDLE] = block


def make_player(x):
    player = {
        'tower': [],
        'inventory': [],
        'selected_block': None,
        'x': x,
    }
    add_block(BLOCK_BASIC, player)
    add_block(BLOCK_BASIC, player)
    add_block(BLOCK_BASIC, player)
    return player


player1 = make_player(PLAYER_1_X)
player2 = make_player(PLAYER_2_X)


def draw():
    screen.clear()
    for player in [player1, player2]:
        for block in player['tower']:
            block.draw()
        if player['selected_block']:
            player['selected_block'].draw()
        for block in player['inventory']:
            if block:
                block.draw()

def update():
    pass


def on_key_down(key):
    if key == keys.S and not player1['selected_block']:
        drop_block(player1, select_block(player1))
    if key == keys.K and not player2['selected_block']:
        drop_block(player2, select_block(player2))



def select_block(player):
    block = player['inventory'][INVENTORY_MIDDLE]
    player['inventory'][INVENTORY_MIDDLE] = None
    player['selected_block'] = block
    return player['selected_block']


def drop_block(player, block):
    y = HEIGHT - (len(player['tower']) * block.height + block.height / 2)
    animate(block, y=y, on_finished=add_dropped_blocks_to_tower)


def add_dropped_blocks_to_tower():
    for player in [player1, player2]:
        if not player['selected_block']:
            continue
        player['tower'].append(player['selected_block'])
        player['selected_block'] = None
        add_block(BLOCK_BASIC, player)