# Stacky Tower
WIDTH = 600
HEIGHT = 800

HALF_WIDTH = WIDTH / 2
PLAYER_1_X = HALF_WIDTH - HALF_WIDTH / 2
PLAYER_2_X = HALF_WIDTH + HALF_WIDTH / 2

BLOCK_BASIC = 'block_basic'


def make_block(block_type):
    return Actor(block_type, pos=(WIDTH / 2, 0))


def make_player(x):
    return {
        'tower': [],
        'inventory': [
            make_block(BLOCK_BASIC),
            make_block(BLOCK_BASIC),
            make_block(BLOCK_BASIC)
        ],
        'selected_block': None,
        'x': x,
    }


player1 = make_player(PLAYER_1_X)
player2 = make_player(PLAYER_2_X)


def draw():
    screen.clear()
    for player in [player1, player2]:
        for block in player['tower']:
            block.draw()
        if player['selected_block']:
            player['selected_block'].draw()


def update():
    pass


def on_key_down(key):
    if key == keys.A:
        drop_block(player1, select_block(player1))
    if key == keys.K:
        drop_block(player2, select_block(player2))



def select_block(player):
    block = player['inventory'].pop()
    block.x = player['x']
    player['selected_block'] = block
    player['inventory'].insert(0, make_block(BLOCK_BASIC))
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