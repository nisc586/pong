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
DEFAULT_BAT_POSITION = Position(MIDDLE.x - BAT_SIZE.width // 2, SCREEN_SIZE.height - BAT_SIZE.height - MARGIN)

DEFAULT_BALL_POSITION = (MIDDLE.x, SCREEN_SIZE.height - 100)
BALL_SIZE = Size(10, 10)
BALL_SPEED_FACTOR = 0.5  # Multiplier for ball speed when it collides with the bat
DEFAULT_BALL_SPEED = 5

BOX_SIZE = Size(60, 20)

TEXT_SIZE = 40
TEXT_POSITION = Position(MIDDLE.x, MIDDLE.y)
TEXT_PADDING = 20

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
            self.movement.x += bat.speed * BALL_SPEED_FACTOR
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


class Menu():
    def __init__(self):
        self.font = pg.font.SysFont("corbel", TEXT_SIZE, bold=True)
        self.message = "Press SPACE to start the game!"
    
    def get_image(self):
        surf = self.font.render(self.message, True, RGB_BLACK, RGB_WHITE)
        padded_surf = surf# pg.transform.scale(surf, (surf.get_width() + TEXT_PADDING, surf.get_height() + TEXT_PADDING))
        return padded_surf


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
    menu = Menu()

    allsprites = pg.sprite.Group(ball, bat)
    allboxes = pg.sprite.Group([box])

    show_menu = True
    menu_image = menu.get_image()

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
                if show_menu:
                    show_menu = False
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

        if len(allboxes) == 0:
            show_menu=True
            ball.reset()
            allboxes.add(box)

        # Render graphics here
        screen.blit(background, (0, 0))

        if show_menu:
            textpos = menu_image.get_rect(centerx=TEXT_POSITION.x, y=TEXT_POSITION.y)
            screen.blit(menu_image, textpos)
        else:
            allboxes.draw(screen)

        allsprites.draw(screen)
        pg.display.flip()
        clock.tick(60)

            
if __name__ == "__main__":
    main()