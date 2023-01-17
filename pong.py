import pygame as pg
from collections import namedtuple
from random import randint, choice

Position = namedtuple("Position", "x y")
Size = namedtuple("Size", "width height")

GAME_TITLE = "Pong"

SCREEN_SIZE = Size(1200, 900)
MIDDLE = Position(600, 450)
MARGIN = 50

BAT_SIZE = Size(15, 200)
BAT_SPEED = 7

BALL_SIZE = Size(15, 15)
BALL_SPEED = 10

TEXT_SIZE = 40
TEXT_POSITION = Position(MIDDLE.x, 10)

BLACK = pg.Color("black")
WHITE = pg.Color("white")


class Bat(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BAT_SIZE)
        self.image.fill(WHITE)
        self.rect = pg.Rect(position, (self.image.get_width(),self.image.get_height()))
        self.speed = BAT_SPEED
    
    def move(self, up=False, down=False):
        """Move the bat up or down, but not outside the screen"""
        if up and not self.rect.top <= 0:
                self.rect.move_ip(0, -self.speed)
        if down and not self.rect.bottom >= SCREEN_SIZE.height:
            self.rect.move_ip(0, self.speed)


class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(BALL_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(MIDDLE,(self.image.get_width(),self.image.get_height()))

        self.reset()
 
    def move(self):
        """Move the ball, bounce of the top or bottom of screen"""
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_SIZE.height:
            self.movement.y = -self.movement.y
        
        self.rect.move_ip(self.movement.x, self.movement.y)
    
    def collide(self, bat):
        """Change direction if the ball collides with a bat"""
        if self.rect.colliderect(bat.rect):
            self.movement.x = - self.movement.x

    def is_outside_screen_left(self):
        """Return True if the ball is outside the left side of the screen"""
        return self.rect.left <= 0
    
    def is_outside_screen_right(self):
        """Return True if the ball is outside the right side of the screen"""
        return self.rect.right >= SCREEN_SIZE.width

    def reset(self):
        """Set position of the ball to the middle of screen and change direction"""
        self.set_position(MIDDLE)
        self.set_random_direction()

    def set_position(self, position):
        self.rect.center = position
    
    def set_random_direction(self):
        """Set movement of the ball to a random direction, that goes left or right"""
        self.movement = pg.math.Vector2(BALL_SPEED, 0)
        self.movement *= choice([-1, 1])
        self.movement.rotate_ip(randint(-60, 60))


class Scoreboard():
    def __init__(self):
        self.score_left = self.score_right = 0
        self.font = pg.font.SysFont("corbel", TEXT_SIZE, bold=True)
    
    def get_text(self):
        """Return the font and the score"""
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
    background.fill(BLACK)

    ball = Ball()
    bat_left = Bat((MARGIN, MIDDLE.y))
    bat_right = Bat((SCREEN_SIZE.width - MARGIN - BAT_SIZE.width, MIDDLE.y))
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
            scoreboard.point_right()
            ball.reset()
        elif ball.is_outside_screen_right():
            scoreboard.point_left()
            ball.reset()

        ball.collide(bat_left)
        ball.collide(bat_right)
        ball.move()

        # Render graphics here
        #---------------------
        screen.blit(background, (0, 0))

        font, text = scoreboard.get_text()
        text_surface = font.render(text, True, WHITE)
        textpos = text_surface.get_rect(centerx=TEXT_POSITION.x, y=TEXT_POSITION.y)
        screen.blit(text_surface, textpos)

        allsprites.draw(screen)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()