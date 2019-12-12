# Stacky Tower
import random
import pygame.transform

WIDTH = 480
HEIGHT = 640

# People with custom keyboard layouts can alter this to their liking.
P1_LEFT = keys.A
P1_DROP = keys.S
P1_RIGHT = keys.D

P2_LEFT = keys.J
P2_DROP = keys.K
P2_RIGHT = keys.L

# Some of the block images are bigger than this, but the actual block
# in the game is considered 32 pixels high (this allows some blocks to
# visually overlap with others).
BLOCK_HEIGHT = 32

# The y coordinate on the screen where the finish line should be
FINISH_LINE = 128

# Various attributes are set on each Player during game setup and
# they are updated as the game progresses.
class Player:
    """Just a namespace for storing global state about players"""
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

def flip_actor_image(actor):
    """This is a hack to flip actor images.

    Only works with the version of PyGame Zero bundled with Mu.
    """
    actor._surf = pygame.transform.flip(actor._orig_surf, True, False)

def make_inventory(player):
    """Makes a starting inventory to show on screen, centered on the towerx
    value."""
    inventory = [
        Actor('basic_icon'), Actor('basic_icon'), Actor('basic_icon')]
    for actor in inventory:
        if player.facing_left:
            flip_actor_image(actor)
    inventory[1].pos = (player.towerx, 50)
    inventory[0].pos = (inventory[1].x - inventory[1].width, inventory[1].y)
    inventory[2].pos = (inventory[1].x + inventory[1].width, inventory[1].y)
    return inventory

# These are the starting block inventories for both players. These blocks may
# be dropped onto their towers.
player1.inventory = make_inventory(player1)
player2.inventory = make_inventory(player2)

# This dictionary maps icon images to full block images, used when blocks are
# dropped from the inventory.
full_block_map = {
    'cannon_icon': 'cannon',
    'ice_icon': 'snowball_cannon',
    'small_shield_icon': 'small_shield_icon',
    'basic_icon': 'basic',
    'shotgun_icon': 'shotgun',
    'medkit_icon': 'medkit',
    'gift_icon': 'gift',
}

# This dictionary maps block images to their damaged images.
damaged_block_map = {
    'basic': 'basic_damaged',
    'cannon': 'cannon_damaged',
    'snowball_cannon': 'snowball_cannon_damaged',
    'shotgun': 'shotgun_damaged',
    'medkit': 'medkit_damaged',
    'small_shield_icon': 'small_shield_icon_damaged',
    'gift': 'gift_damaged',
}
# This dictionary maps damaged blocks back to their original values (when healed).
healed_block_map = dict((value, key) for key, value in damaged_block_map.items())

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

# Each player may have shields protecting their towers.
player1.shields = []
player2.shields = []

# Cannon balls flying toward a target tower
shots_fired = []

# Cannon balls that missed their target and will eventually
# fly off screen.
shots_missed = []

# In the game, press / to show debug info
debug = False

show_menu = True
show_instructions = False
menu_options = [
    "How to play",
    "1 player",
    "2 players",
]
selected_option = 0

active_player = player1
active_player_marker = Actor('active_player')
active_player_marker.x = player1.towerx
active_player_marker.y = 20

# The winner of the game
winner = None

# When medkits are dropped, their healing power drifts down the tower.
# Each medkit creates an Actor and adds it here.
medkit_heals = []
gifts = []
# This flag controls the 1-player version of the game. If this flag is
# True then player 2 is controlled by an "AI".
player2.is_ai = False

def draw():
    screen.blit('background_winter', (0, 0))
    active_player_marker.draw()
    draw_later = []
    for block in player1.tower:
        if block.image != 'small_shield':
            block.draw()
            if block.iced:
                ice = Actor('iced', pos=block.pos)
                ice.draw()
    for block in player2.tower:
        if block.image != 'small_shield':
            block.draw()
            if block.iced:
                ice = Actor('iced', pos=block.pos)
                ice.draw()

    # Now that the two towers have most of their blocks drawn,
    # we can draw the small shields which have to be drawn on
    # top of other block
    for small_shield in player1.shields + player2.shields:
        small_shield.draw()
    for block in player1.inventory:
        block.draw()
    for block in player2.inventory:
        block.draw()
    if player1.falling_block:
        player1.falling_block.draw()
    if player2.falling_block:
        player2.falling_block.draw()
    if debug:
        debug_text("shots_fired: {}", 80, len(shots_fired))
        debug_text("shots_missed: {}", 100, len(shots_missed))
        debug_text("Player 1 tower height: {}", 120, len(player1.tower))
        debug_text("Player 2 tower height: {}", 140, len(player2.tower))

    selector1.draw()
    selector2.draw()
    # draw the finish line
    for i in range(8, WIDTH, 32):
        screen.draw.line(
            (i, FINISH_LINE), (i + 16, FINISH_LINE), (255, 32, 32))
    for cannon_ball in shots_fired + shots_missed:
        cannon_ball.draw()
    for snowball in shots_fired + shots_missed:
        snowball.draw()
    for medkit_heal in medkit_heals:
        medkit_heal.draw()
    if winner:
        if winner is player1:
            winner_name = "Player 1"
        else:
            winner_name = "Player 2"
        screen.draw.filled_rect(Rect(
            (WIDTH // 8, HEIGHT / 3),
            (WIDTH - WIDTH // 4, HEIGHT / 3)),
            (255, 255, 255))
        screen.draw.text("{} is the winner!\nPRESS ANY KEY FOR MAIN MENU".format(winner_name),
                         center=(WIDTH // 2, HEIGHT // 2),
                         color=(255, 0, 0),
                         fontsize=32,
                         fontname="1980xx")
    if show_menu:
        draw_menu()

def debug_text(msg, y, *args):
    screen.draw.text(msg.format(*args), (10, y), color=(255, 0, 0), fontname="1980xx")

def replace_block(player):
    """Replaces the previously selected block with a new random block."""
    value = random.random()
    if value > 0.3:
        new_block_image = random.choice(['shotgun_icon', 'cannon_icon', 'basic_icon', 'ice_icon'])
    else:
        new_block_image = random.choice(['medkit_icon', 'small_shield_icon', 'gift_icon'])
    new_block = Actor(new_block_image)
    if player.facing_left:
        flip_actor_image(new_block)
    new_block.x = player.towerx
    new_block.y = 50
    player.inventory[player.selected_block] = new_block

def drop_selected_block(player):
    """Drops the selected block in the inventory."""
    block = prepare_for_drop(
        player, player.inventory[player.selected_block])
    player.falling_block = block
    fall_onto_player_tower(block, player)

def prepare_for_drop(player, block):
    block.damaged = False
    block.iced = False
    block.x = player.towerx
    block.image = full_block_map[block.image]
    if player.facing_left:
        flip_actor_image(block)
    return block

def fall_onto_player_tower(block, player):
    """Animates the fall of the block onto the player's tower."""
    block.target_y = get_tower_top_y(player)
    duration = calculate_fall_duration(block.y, block.target_y)
    animate(block, duration=duration, y=block.target_y,
            on_finished=resolve_drop)

def calculate_fall_duration(start_y, end_y):
    """Returns the length of time in seconds that it should take
    to fall from start_y to end_y."""
    return 0.8 * ((end_y - start_y) / HEIGHT)

def resolve_drop():
    """Finishes the drop if block lands on tower, or makes it keep falling.

    This is needed because the tower height might have changed since the block
    was originally dropped."""
    for player in [player1, player2]:
        if player.falling_block and (
                player.falling_block.y == player.falling_block.target_y):
            # this is how far the block was supposed to fall
            # now see if it's actually on the tower (or maybe the tower
            # height changed while it was falling and it needs to fall more)
            if player.falling_block.y == get_tower_top_y(player):
                # it's on the top of the tower
                finish_drop(player)
            else:
                # the tower height must have changed - keep falling
                fall_onto_player_tower(player.falling_block, player)

def finish_drop(player):
    """Finishes processing the dropped block for the given player.

    Adds the block to their tower, removes the falling block, etc.

    Also triggers special actions for certain blocks.
    """
    player.tower.append(player.falling_block)

    if len(player.tower) > 1 and player.tower[-2].iced:
        finish_drop0_2(player)
        return
    if player.falling_block.image == 'cannon':
        fire_cannon(player, player.falling_block)
    elif player.falling_block.image == 'shotgun':
        fire_shotgun(player, player.falling_block)
    elif player.falling_block.image == 'medkit':
        heal_tower(player, player.falling_block)
    elif player.falling_block.image == 'small_shield_icon':
        make_small_shield(player, player.falling_block)
    elif player.falling_block.image == 'basic':
        sounds.block_land.play()
    elif player.falling_block.image == 'gift':
        give_gift(player)
    elif player.falling_block.image == 'snowball_cannon':
        fire_snowball_cannon(player, player.falling_block)
    finish_drop0_2(player)
def finish_drop0_2(player):
    global winner, active_player
    player.falling_block = None
    if is_winner(player):
        winner = player
    if active_player is player1:
        active_player = player2
    else:
        active_player = player1
    animate(active_player_marker, duration=0.4, x=active_player.towerx, tween='accelerate', on_finished=do_ai_move)

def give_gift(player):
    target_block = player.tower[-2]
    if target_block.image == 'cannon':
        fire_cannon(player, target_block)
    elif target_block.image == 'shotgun':
        fire_shotgun(player, target_block)
    elif target_block.image == 'medkit':
        heal_tower(player, target_block)
    elif target_block.image == 'small_shield_icon':
        make_small_shield(player, target_block)
    elif target_block.image == 'snowball_cannon':
        fire_snowball_cannon(player, target_block)
def do_ai_move():
    """Selects a random block from the inventory."""
    if not winner and active_player is player2 and player2.is_ai:
        new_block = random.randint(0,2)
        difference = abs(new_block - player2.selected_block)
        for i in range(difference):
            if new_block > player2.selected_block:
                switch_selected_block(player2, -1)
            elif new_block < player2.selected_block:
                switch_selected_block(player2, 1)
        clock.schedule(drop_ai_block, 0.1)

def drop_ai_block():
    """Triggers a block drop for the AI."""
    drop_selected_block(player2)
    replace_block(player2)

def is_winner(player):
    """Returns True if the player has won."""
    return not winner and (
        get_tower_top_y(player) < FINISH_LINE - BLOCK_HEIGHT // 2)

def fire_cannon(player, cannon_block):
    """Fires a cannon ball for the player out of the cannon_block."""
    cannon_ball = Actor('cannon_ball', pos=cannon_block.pos)
    sounds.cannon_boom.play()
    target, end_shot_x = get_target_player_and_x(player, cannon_block)
    shots_fired.append(cannon_ball)
    cannon_ball.target_player = target
    animate(cannon_ball, x=end_shot_x)
def fire_snowball_cannon(player, snowball_cannon_block):
    snowball = Actor('snowball', pos=snowball_cannon_block.pos)
    target, end_shot_x = get_target_player_and_x(player, snowball_cannon_block)
    shots_fired.append(snowball)
    snowball.target_player = target
    animate(snowball, x=end_shot_x)
def get_target_player_and_x(attacker, attack):
    if attacker is player1:
        return player2, WIDTH + attack.width
    else:
        return player1, -attack.width

def fire_shotgun(player, shotgun):
    """Fires a shotgun blast for the player.

    The variable passed as shotgun should be a block.
    """
    target, end_shot_x = get_target_player_and_x(player, shotgun)
    sounds.shotgun_boom.play()
    for i in range(-4, 5, 2):
        shot = Actor('shotgun_shot')
        shot.y = shotgun.y
        if player.facing_left:
            shot.x = shotgun.x - 15
        else:
            shot.x = shotgun.x + 15
        shots_fired.append(shot)
        shot.target_player = target
        animate(shot, duration=random.uniform(0.4, 0.5), x=end_shot_x, y=shotgun.y + BLOCK_HEIGHT * i)

def heal_tower(player, medkit):
    """Triggers a medkit heal action that drifts down the tower."""
    medkit_heal = Actor('medkit_heal', pos=medkit.pos)
    sounds.heal.play()
    medkit_heals.append(medkit_heal)
    target_y = medkit.y + BLOCK_HEIGHT * 3
    medkit_heal.target_y = target_y
    medkit_heal.medkit = medkit
    animate(medkit_heal, y=target_y, on_finished=cleanup_medkits)
def ice_tower(player, target_block):
    target_block.iced = True

def make_small_shield(player, small_shield_icon):
    """Puts a small shield on the tower near small_shield_icon."""
    small_shield = Actor('small_shield', pos=small_shield_icon.pos)
    if player.facing_left:
            flip_actor_image(small_shield)
    small_shield_icon.shield = small_shield
    sounds.small_shield_on.play()
    player.shields.append(small_shield)
    small_shield.damaged = False

def cleanup_medkits():
    """Cleans up medkit heal actions that have completed."""
    for medkit_heal in list(medkit_heals):
        if medkit_heal.y == medkit_heal.target_y:
            medkit_heals.remove(medkit_heal)

def get_tower_top_y(player):
    """Returns the y coordinate of the top of the tower."""
    return HEIGHT - len(player.tower) * BLOCK_HEIGHT - BLOCK_HEIGHT // 2

def update():
    global small_shield, small_shield_healths, small_shield_health
    # check missed shots to see if they go off screen
    for shot in list(shots_missed):
        if shot.x >= WIDTH or shot.x <= 0:
            shots_missed.remove(shot)

    # Handles all shotgun and cannon hits against towers.
    players_with_lost_blocks = set()
    for shot in list(shots_fired):
        if is_not_close_enough(shot):
            # ignore for now - shot still flying toward target
            continue
        elif is_hit_possible(shot):
            # the tower is tall enough to be hit - check for hit
            for block in list(shot.target_player.tower):
                if block.collidepoint(shot.pos):
                    shots_fired.remove(shot)
                    sounds.block_damage.play()
                    if shot.image == 'snowball':
                        ice_tower(shot.target_player, block)
                    elif shot.image == 'cannon_ball' or block.damaged:
                        shot.target_player.tower.remove(block)
                        players_with_lost_blocks.add(shot.target_player)
                    elif shot.image == 'shotgun_shot' and block.image in damaged_block_map:
                        block.image = damaged_block_map[block.image]
                        if shot.target_player.facing_left:
                            flip_actor_image(block)
                        block.damaged = True
        else:
            # it's a miss
            shots_fired.remove(shot)
            shots_missed.append(shot)
    # Handles all shotgun and cannon shots against shields
    # TODO: roll this into general shot handling above
    for shot in list(shots_fired):
        for player in [player1, player2]:
            for small_shield in list(player.shields):
                if small_shield.collidepoint(shot.pos):
                    sounds.block_damage.play()
                    if shot in shots_fired:
                        shots_fired.remove(shot)
                    if shot.image == 'cannon_ball' or small_shield.damaged:
                        player.shields.remove(small_shield)
                    else:
                        small_shield.damaged = True
                        small_shield.image = 'small_shield_damaged'
                        if small_shield.x > WIDTH/2:
                            flip_actor_image(small_shield)
    # Cause blocks to fall if ones below them were destroyed.
    for player in players_with_lost_blocks:
        target_y = HEIGHT - BLOCK_HEIGHT // 2
        for block in player.tower:
            if block.y != target_y:
                # It needs to fall
                fall_duration = calculate_fall_duration(block.y, target_y)
                if block.image == 'small_shield_icon':
                    animate(block.shield, y=target_y, duration=fall_duration)
                animate(block, y=target_y, duration=fall_duration)
            target_y -= BLOCK_HEIGHT
    # Perform healing actions as medkit heal actions move down the tower.
    for medkit_heal in medkit_heals:
        for player in [player1, player2]:
            for block in player.tower:
                if block.collidepoint(medkit_heal.pos):
                    if block.damaged:
                        block.image = healed_block_map[block.image]
                        if player.facing_left:
                            flip_actor_image(block)
                    block.damaged = False



def is_not_close_enough(cannon_ball):
    """Returns True if the ball hasn't reached the tower yet."""
    if cannon_ball.target_player is player1:
        return cannon_ball.x > cannon_ball.target_player.towerx
    else:
        return cannon_ball.x < cannon_ball.target_player.towerx

def is_hit_possible(cannon_ball):
    """Returns True if the ball is near a tower that is tall enough to hit."""
    target_top_y = get_tower_top_y(cannon_ball.target_player)
    if debug:
        print("target_top_y: {}, cannon_ball.y: {}"
            .format(target_top_y, cannon_ball.y))
    tower_left_x = cannon_ball.target_player.towerx - BLOCK_HEIGHT // 2
    tower_right_x = cannon_ball.target_player.towerx + BLOCK_HEIGHT // 2
    return (target_top_y <= cannon_ball.y
        and tower_left_x <= cannon_ball.x <= tower_right_x)

def reset_game():
    global show_menu, active_player, winner
    show_menu = True
    for player in [player1, player2]:
        player.tower.clear()
        player.shields.clear()
        player.inventory = make_inventory(player)
        player.selected_block = 1
    player2.is_ai = False
    active_player = player1
    active_player_marker.x = player1.towerx
    winner = False

def on_key_down(key):
    global debug, show_menu, selected_option, show_instructions
    if winner:
        reset_game()
        return
    if show_instructions:
        show_instructions = False
        return
    if show_menu:
        if key == keys.RETURN:
            if selected_option == 1:
                player2.is_ai = True
                show_menu = False
            elif selected_option == 0:
                show_instructions = True
            else:
                show_menu = False
        elif key == keys.DOWN:
            selected_option += 1
            if selected_option > 2:
                selected_option = 0
        elif key == keys.UP:
            selected_option -= 1
            if selected_option < 0:
                selected_option = 2
        return
    # When P1_DROP is pressed, add a block for player 1
    if key == P1_DROP and not player1.falling_block and (debug or active_player is player1):
        drop_selected_block(player1)
        replace_block(player1)
    # When P2_DROP is pressed, add a block for player 2
    elif key == P2_DROP \
            and not player2.falling_block \
            and not player2.is_ai \
            and (debug or active_player is player2):
        drop_selected_block(player2)
        replace_block(player2)

    elif key == P1_LEFT and player1.selected_block < 2:
        # Move player1 selected block left
        switch_selected_block(player1, -1)
    elif key == P1_RIGHT and player1.selected_block > 0:
        # Move player1 selected block right
        switch_selected_block(player1, 1)

    elif key == P2_LEFT and not player2.is_ai and player2.selected_block < 2:
        # Move player2 selected block left
        switch_selected_block(player2, -1)
    elif key == P2_RIGHT and not player2.is_ai and player2.selected_block > 0:
        # Move player2 selected block right
        switch_selected_block(player2, 1)

    elif key == keys.SLASH:
        debug = not debug

    elif debug and key == keys.K_1:
        test_scenario_1()

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

def draw_menu():
    box_top = HEIGHT // 4 * .7
    box_left = WIDTH // 4
    title_top = box_top + 10
    screen.draw.filled_rect(Rect(
            (box_left, box_top),
            (WIDTH - WIDTH // 2, HEIGHT * .70)),
        (0, 0, 0))
    screen.draw.text("STACKY TOWER",
        centerx=WIDTH // 2,
        centery=title_top + 20,
        fontname="1980xx",
        fontsize=32)
    if show_instructions:
        draw_instructions(title_top + 40, box_left + 10)
        return
    for i, text in enumerate(menu_options):
        if i == selected_option:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        screen.draw.text(text,
            centerx=WIDTH // 2,
            centery=title_top + i * 30 + 80,
            fontname="1980xx", color=color, fontsize=28)
    screen.draw.text("(Up/Down to change\nEnter to select)",
        centerx=WIDTH // 2, centery=title_top + i * 30 + 180,
        fontname="1980xx", color=(0, 255, 0))

def draw_instructions(top, left):
    instructions = """\
Left player
  Slide Block Left: A
  Slide Block Right: D
  Drop Selected Block: S

Right player
  Slide Block Left: J
  Slide Block Right: L
  Drop Selected Block: K

Left player goes first.
Be the first to cross
the finish line. Use
attacks to destroy
opponent tower. Place
shields to defend and
heal blocks with medkits.

    """
    screen.draw.text(instructions, topleft=(left, top),
        fontname="1980xx")
    screen.draw.text("(Press any key to continue)",
        centerx=WIDTH // 2, centery=550,
        fontname="1980xx", color=(0, 255, 0))

def test_scenario_1():
    player1.tower = []
    for i in range(10):
        block = Actor('basic_icon')
        block.y = get_tower_top_y(player1)
        player1.tower.append(prepare_for_drop(player1, block))