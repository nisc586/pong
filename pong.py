import pygame as pg

GAME_TITLE = "Pong"
SCREEN_SIZE = (1200, 900)
MIDDLE = (600, 450)
MARGIN = 50

BAT_SIZE = (50, 350)
BAT_SPEED = 10

BALL_SIZE = (50, 50)
BAT_SPEED = 5

RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)


class Bat(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BAT_SIZE)
        self.image.fill(RGB_WHITE)
        self.rect = pg.Rect(position, (self.image.get_width(),self.image.get_height()))
        self.speed = BAT_SPEED
    
    def move(self, up=False, down=False):
        if up:
            self.rect.move_ip(0, self.speed)
        if down:
            self.rect.move_ip(0, -self.speed)

class Ball(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BALL_SIZE)
        self.image.fill(RGB_WHITE)
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(position,(self.image.get_width(),self.image.get_height()))


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    pg.display.set_caption(GAME_TITLE)
    pg.mouse.set_visible(False)

    clock = pg.time.Clock()

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_BLACK)

    ball = Ball(MIDDLE)
    bat_left = Bat((MARGIN, MIDDLE[1]))
    bat_right = Bat((SCREEN_SIZE[0] - MARGIN - BAT_SIZE[0], MIDDLE[1]))

    allsprites = pg.sprite.Group(ball, bat_left, bat_right)

    while True:
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            bat_left.move(up=True)
        if keys[pg.K_s]:
            bat_left.move(down=True)
        if keys[pg.K_UP]:
            bat_right.move(up=True)
        if keys[pg.K_DOWN]:
            bat_right.move(down=True)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
        
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()