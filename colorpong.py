import pygame as pg
import random
from collections import namedtuple


Position = namedtuple("Position", "x y")
Size = namedtuple("Size", "width height")

GAME_TITLE = "Boxpong"

SCREEN_SIZE = Size(1200, 900)
MIDDLE = Position(600, 450)
MARGIN = 10

NOSSLE_POSITION = Position(MIDDLE.x, MARGIN)

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

class Nossle:
    pass


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)

    background = pg.Surface(screen.get_size())
    background.fill(BACKGROUND_COLOR)

    positions_x = [100, 150, 200, 250, 300,  350]
    balls = pg.sprite.Group([Ball((pos, MIDDLE.y), col) for pos, col in zip(positions_x, BALL_COLORS)])

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
        pg.display.flip()


if __name__ == "__main__":
    main()