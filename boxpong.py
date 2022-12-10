import pygame as pg
from collections import namedtuple

Position = namedtuple("Position", "x y")
Size = namedtuple("Size", "width height")

GAME_TITLE = "Boxpong"

SCREEN_SIZE = Size(1200, 900)
MIDDLE = Position(600, 450)
MARGIN = 10

BAT_SIZE = Size(100, 20)
MAX_BAT_SPEED = 10
BAT_ACCELERATION = 0.75
DEFAULT_BAT_POSITION = Position(MIDDLE.x, SCREEN_SIZE.height - BAT_SIZE.height - MARGIN)

DEFAULT_BALL_POSITION = (MIDDLE.x, SCREEN_SIZE.height - 100)
BALL_SIZE = Size(10, 10)
DEFAULT_BALL_SPEED = 5

BOX_SIZE = Size(60, 20)

TEXT_SIZE = 40
TEXT_POSITION = Position(MIDDLE.x, 10)

RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)

class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BALL_SIZE)
        self.rect = pg.draw.circle(surface=self.image, color=RGB_WHITE, center=(BALL_SIZE.width // 2, BALL_SIZE.height // 2), radius=BALL_SIZE.width // 2)
        self.reset()
    
    def move(self):
        if self.rect.top <= 0:
            self.movement.y = -self.movement.y
        elif self.rect.left <= 0:
            self.movement.x = -self.movement.x
        elif self.rect.right >= SCREEN_SIZE.width:
            self.movement.x = -self.movement.x
        
        self.rect.move_ip(self.movement.x, self.movement.y)
    
    def collide(self, bat):
        if self.rect.colliderect(bat.rect):
            self.movement.x += bat.speed
            self.movement.y = -self.movement.y
    
    def collide_box(self, box):
        if self.rect.clipline(box.top_side) or self.rect.clipline(box.bottom_side):
            self.movement.y = - self.movement.y
        elif self.rect.clipline(box.left_side) or self.rect.clipline(box.right_side):
            self.movement.x = - self.movement.x
    
    def reset(self):
        self.rect.center = DEFAULT_BALL_POSITION
        self.movement = pg.math.Vector2((0, 0))
    
    def is_outside_screen(self):
        return self.rect.top >= SCREEN_SIZE.height

class Box(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BOX_SIZE)
        self.image.fill(RGB_WHITE)
        self.rect = pg.Rect(MIDDLE, (self.image.get_width(), self.image.get_height()))
        self.left_side = (self.rect.bottomleft, self.rect.topleft)
        self.right_side = (self.rect.bottomright, self.rect.topright)
        self.top_side = (self.rect.topleft, self.rect.topright)
        self.bottom_side = (self.rect.bottomleft, self.rect.bottomright)
    

class Bat(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(BAT_SIZE)
        self.image.fill(RGB_WHITE)
        self.rect = pg.Rect(DEFAULT_BAT_POSITION, (self.image.get_width(), self.image.get_height()))
        self.speed = 0
    
    def move(self, left=False, right=False):
        if left and not self.rect.left <= 0:
            self.speed = max(self.speed - BAT_ACCELERATION, -MAX_BAT_SPEED)
            self.rect.move_ip(self.speed, 0)
        if right and not self.rect.right >= SCREEN_SIZE.width:
            self.speed = min(self.speed + BAT_ACCELERATION, MAX_BAT_SPEED)
            self.rect.move_ip(self.speed, 0)


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    pg.display.set_caption(GAME_TITLE)
    pg.mouse.set_visible(False)

    clock = pg.time.Clock()

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_BLACK)
    
    ball = Ball()
    bat = Bat()
    box = Box()

    allsprites = pg.sprite.Group(ball, bat)
    allboxes = pg.sprite.Group([box])

    while True:
        # Player input here
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            bat.move(left=True)
        if keys[pg.K_RIGHT]:
            bat.move(right=True)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if ball.movement.magnitude() == 0:
                    ball.movement.y = DEFAULT_BALL_SPEED
            elif event.type == pg.KEYUP and (event.key == pg.K_LEFT or event.key == pg.K_RIGHT):
                bat.speed = 0
        
        # Logical updates here
        if ball.is_outside_screen():
            ball.reset()
        
        target_box = pg.sprite.spritecollide(ball, allboxes, dokill=True)
        if target_box:
            tgb = target_box[0]
            ball.collide_box(tgb)
            del(tgb)

        ball.collide(bat)
        ball.move()

        # Render graphics here
        screen.blit(background, (0, 0))

        allsprites.draw(screen)
        allboxes.draw(screen)
        pg.display.flip()
        clock.tick(60)

            
if __name__ == "__main__":
    main()