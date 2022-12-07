import pygame as pg
from random import randint, choice

GAME_TITLE = "Pong"
SCREEN_SIZE = (1200, 900)
MIDDLE = (600, 450)
MARGIN = 50

BAT_SIZE = (25, 300)
BAT_SPEED = 9

BALL_SIZE = (20, 20)
BALL_SPEED = 7

TEXT_SIZE = 40
TEXT_POSITION = (MIDDLE[0], 10)

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
        if up and not self.rect.top <= 0:
                self.rect.move_ip(0, -self.speed)
        if down and not self.rect.bottom >= SCREEN_SIZE[1]:
            self.rect.move_ip(0, self.speed)


class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(BALL_SIZE)
        self.image.fill(RGB_WHITE)
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(MIDDLE,(self.image.get_width(),self.image.get_height()))

        self.reset()
 
    def move(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_SIZE[1]:
            self.movement.y = -self.movement.y
        
        self.rect.move_ip(self.movement.x, self.movement.y)
    
    def collide(self, bat):
        if self.rect.colliderect(bat.rect):
            self.movement.x = - self.movement.x

    def is_outside_screen_left(self):
        return self.rect.left <= 0
    
    def is_outside_screen_right(self):
        return self.rect.right >= SCREEN_SIZE[0]

    def reset(self):
        self.set_position(MIDDLE)
        self.set_random_direction()

    def set_position(self, position):
        self.rect.center = position
    
    def set_random_direction(self):
        self.movement = pg.math.Vector2(BALL_SPEED, 0)
        
        self.movement *= choice([-1, 1])
        self.movement.rotate_ip(randint(-60, 60))


class Scoreboard():
    def __init__(self):
        self.score_left = self.score_right = 0
        self.font = pg.font.SysFont("corbel", TEXT_SIZE, bold=True)
    
    def get_text(self):
        text = f"{self.score_left} : {self.score_right}"
        return self.font, text
    
    def point_left(self):
        self.score_left += 1
    
    def point_right(self):
        self.score_right += 1
        

def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    pg.display.set_caption(GAME_TITLE)
    pg.mouse.set_visible(False)

    clock = pg.time.Clock()

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_BLACK)

    ball = Ball()
    bat_left = Bat((MARGIN, MIDDLE[1]))
    bat_right = Bat((SCREEN_SIZE[0] - MARGIN - BAT_SIZE[0], MIDDLE[1]))
    scoreboard = Scoreboard()

    allsprites = pg.sprite.Group(ball, bat_left, bat_right)

    while True:
        # Player input here
        #------------------
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
        
        # Logical updates here
        #---------------------
        if ball.is_outside_screen_left():
            scoreboard.point_left()
            ball.reset()
        elif ball.is_outside_screen_right():
            scoreboard.point_right()
            ball.reset()

        ball.collide(bat_left)
        ball.collide(bat_right)
        ball.move()

        # Render graphics here
        #---------------------
        screen.blit(background, (0, 0))

        font, text = scoreboard.get_text()
        text_surface = font.render(text, True, RGB_WHITE)
        textpos = text_surface.get_rect(centerx=TEXT_POSITION[0], y=TEXT_POSITION[1])
        screen.blit(text_surface, textpos)

        allsprites.draw(screen)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()