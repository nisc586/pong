import pygame as pg

import random
from collections import namedtuple


Position = namedtuple("Position", "x y")
Size = namedtuple("Size", "width height")

GAME_TITLE = "Colorpong"

SCREEN_SIZE = Size(1200, 900)
MIDDLE = Position(600, 450)
MARGIN = 20

NOZZLE_SIZE = Size(20, 20)
NOZZLE_RADIUS = 50
NOZZLE_RADIAL_SPEED = 3
NOZZLE_POSITION = Position(MIDDLE.x, SCREEN_SIZE.height - MARGIN)

BACKGROUND_COLOR = pg.Color("black")

BALL_SIZE = Size(30, 30)
BALL_COLORS = [pg.Color(s) for s in ("red", "blue", "green", "yellow", "orange", "purple")]
DEFAULT_BALL_SPEED = 10

BALL_TREE_ROWS = 20
BALL_TREE_COLS = 20

class Ball(pg.sprite.Sprite):
    def __init__(self, position, color=None):
        pg.sprite.Sprite.__init__(self)

        if color not in BALL_COLORS:
            self.color = random.choice(BALL_COLORS)
        else:
            self.color = color
        self.image = pg.Surface(BALL_SIZE)
        self.rect = pg.draw.circle(surface=self.image, color=self.color, center=(BALL_SIZE.width // 2, BALL_SIZE.height // 2), radius=BALL_SIZE.width // 2)
        self.rect.center = position

        self.movement = pg.math.Vector2(0, 0)
    
    def move(self):
        if self.rect.top <= MARGIN:
            self.movement = pg.math.Vector2(0, 0)
            self.rect.centery = MARGIN
        elif self.rect.right >= SCREEN_SIZE.width:
            self.movement.x = -self.movement.x
        elif self.rect.left <= MARGIN:
            self.movement.x = -self.movement.x
        elif self.rect.bottom > SCREEN_SIZE.height:
            raise AssertionError("Unreachable")
        
        self.rect.move_ip(self.movement.x, self.movement.y)


class Nozzle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.anchor = pg.math.Vector2(NOZZLE_POSITION)
        self.offset = pg.math.Vector2(0, -NOZZLE_RADIUS)

        self.image = pg.Surface(NOZZLE_SIZE)
        pg.draw.polygon(self.image, pg.Color("white"), 
            [(0, NOZZLE_SIZE.height), (NOZZLE_SIZE.width, NOZZLE_SIZE.height), (NOZZLE_SIZE.width // 2, 0)])
        self.original = self.image

        self.rect = self.image.get_rect(center=self.anchor + self.offset)

        self.rotation = 0

    def turn(self, left=False, right=False):
        if left:
            self.rotation = min(self.rotation + NOZZLE_RADIAL_SPEED, 80)
        elif right:
            self.rotation = max(self.rotation - NOZZLE_RADIAL_SPEED, -80)
        
        rotated_offset = self.offset.rotate(-self.rotation)
        self.image = pg.transform.rotate(self.original, self.rotation)
        self.rect = self.image.get_rect(center=self.anchor + rotated_offset)
    

    def shoot(self, ball):
        ball.movement = pg.math.Vector2(0, -DEFAULT_BALL_SPEED).rotate(-self.rotation)


class BallTree():
    def __init__(self):
        self.matrix = {}

        # Add initial pyramid pattern
        pyramid_width = 10
        for n in range(pyramid_width):
            for m in range(pyramid_width-n):
                color = random.choice(BALL_COLORS)
                pos = self.get_position(
                    row=n,
                    col=(BALL_TREE_COLS - pyramid_width) // 2 + m + (n // 2)
                )
                self.matrix[(n, m)] = Ball(pos, color)
        
        self.group = pg.sprite.Group(self.matrix.values())
    
    def get_position(self, row, col):
        x = MIDDLE.x + (col - BALL_TREE_COLS // 2) * BALL_SIZE.width
        # Add offset for odd rows
        if row % 2 == 1:
            x += BALL_SIZE.width / 2
        y = MARGIN + row * BALL_SIZE.height
        return x, y

    def add_child(self, node, lr):
        pass

    def get_adjacent(self, node):
        pass

    def remove(self, node):
        pass

    def get_parents(self, node):
        pass


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    clock = pg.time.Clock()

    background = pg.Surface(screen.get_size())
    background.fill(BACKGROUND_COLOR)

    balls = pg.sprite.Group([])
    active_ball = Ball(NOZZLE_POSITION, random.choice(BALL_COLORS))
    nozzle = Nozzle()
    playersprites = pg.sprite.Group(nozzle, active_ball)

    ball_tree = BallTree()

    while True:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            nozzle.turn(left=True)
        elif keys[pg.K_RIGHT]:
            nozzle.turn(right=True)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                nozzle.shoot(active_ball)
                playersprites.remove(active_ball)
                balls.add(active_ball)
                active_ball = Ball(NOZZLE_POSITION, random.choice(BALL_COLORS))
                playersprites.add(active_ball)
    
        # Logical updates here
        #---------------------
        for ball in balls:
            ball.move()

        # Render graphics here
        #---------------------
        screen.blit(background, (0, 0))
        balls.draw(screen)
        playersprites.draw(screen)
        ball_tree.group.draw(screen)
        clock.tick(60)
        pg.display.flip()


if __name__ == "__main__":
    main()