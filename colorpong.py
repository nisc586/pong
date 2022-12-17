import pygame as pg

import random
from collections import namedtuple


Position = namedtuple("Position", "x y")
Size = namedtuple("Size", "width height")

GAME_TITLE = "Boxpong"

SCREEN_SIZE = Size(1200, 900)
MIDDLE = Position(600, 450)
MARGIN = 10

NOZZLE_POSITION = Position(MIDDLE.x, SCREEN_SIZE.height - MARGIN)
NOZZLE_SIZE = Size(20, 20)
NOZZLE_RADIUS = 25
NOZZLE_RADIAL_SPEED = 3

BACKGROUND_COLOR = pg.Color("black")


BALL_SIZE = Size(20, 20)
BALL_COLORS = [pg.Color(s) for s in ("red", "blue", "green", "yellow", "orange", "purple")]
DEFAULT_BALL_SPEED = 7


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


class Nozzle(pg.sprite.Sprite):
    def __init__(self, ball):
        pg.sprite.Sprite.__init__(self)
        self.ball = ball

        self.image = pg.Surface(NOZZLE_SIZE)
        bl = Position(0, NOZZLE_SIZE.height)
        br = Position(NOZZLE_SIZE.width, NOZZLE_SIZE.height)
        tip = Position(NOZZLE_SIZE.width // 2, 0)
        self.rect = pg.draw.polygon(self.image, pg.Color("white"), [bl, br, tip])
        self.rect.center = NOZZLE_POSITION

    def turn(self, left=False, right=False):
        pass



def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)

    background = pg.Surface(screen.get_size())
    background.fill(BACKGROUND_COLOR)

    positions_x = [100, 150, 200, 250, 300,  350]
    balls = pg.sprite.Group([Ball((pos, MIDDLE.y), col) for pos, col in zip(positions_x, BALL_COLORS)])
    nozzle = Nozzle(None)
    playersprites = pg.sprite.Group(nozzle)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
    
        # Render graphics here
        #---------------------
        screen.blit(background, (0, 0))
        balls.draw(screen)
        playersprites.draw(screen)
        pg.display.flip()


if __name__ == "__main__":
    main()