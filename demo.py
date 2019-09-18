WIDTH = 320
HEIGHT = 240
SPEED = 5

redbox = Rect((0, 0), (50, 50))
greenbox = Rect((50, 0), (50, 50))
bluebox = Rect((100, 0), (50, 50))

def draw():
    screen.clear()
    screen.draw.filled_rect(redbox, (255, 0, 0))
    screen.draw.filled_rect(greenbox, (0, 255, 0))
    screen.draw.filled_rect(bluebox, (0, 0, 255))

def update():
    for box in [redbox, greenbox, bluebox]:
        if box.y == 0 and box.x < WIDTH - 50:
            box.x += SPEED
        elif box.x == WIDTH - 50 and box.y < HEIGHT - 50:
            box.y += SPEED
        elif box.y == HEIGHT - 50 and box.x > 0:
            box.x -= SPEED
        else:
            box.y -= SPEED