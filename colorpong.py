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

BALL_GRID_ROWS = SCREEN_SIZE.height * 0.75 // BALL_SIZE.height
BALL_GRID_COLS = SCREEN_SIZE.width // BALL_SIZE.width

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


class BallGrid():
    def __init__(self):
        n_columns = (SCREEN_SIZE.width - 2 * MARGIN) // BALL_SIZE.width
        empty_space_left = ((SCREEN_SIZE.width - 2 * MARGIN) - n_columns * BALL_SIZE.width) / 2

        self.center_points = {}
        for i in range(int(BALL_GRID_ROWS)):
            for j in range(n_columns):
                x = empty_space_left + BALL_SIZE.width / 2 + j * BALL_SIZE.width
                if i % 2 == 1:
                    x += BALL_SIZE.width / 2
                y = MARGIN + BALL_SIZE.height / 2 + i * BALL_SIZE.height
                self.center_points[(i, j)] = (x, y)

        self.matrix = {}

        # Add initial pyramid pattern
        pyramid_width = 10
        for n in range(pyramid_width):
            for m in range(pyramid_width-n):
                color = random.choice(BALL_COLORS)
                col =  n + (n_columns - pyramid_width)//2
                pos = self.center_points[(m,col)]
                self.matrix[(m, col)] = Ball(pos, color)
        
        self.group = pg.sprite.Group(self.matrix.values())
    
    @property
    def rects(self):
        return {
            key: value.rect
            for key, value in self.matrix.items()
        }
    

    def add_ball_hit(self, ball, row, col):
        ball.rect.center = self.center_points[(row, col)]
        ball.movement = pg.math.Vector2(0, 0)

        matches = self.get_adjacent_matches(row, col, ball.color, {(row, col)})

        if len(matches) >= 2:
            for key, b in matches:
                del self.matrix[key]
                self.group.remove(b)
        else:
            self.matrix[(row, col)] = ball
            self.group.add(ball)
        
        self.delete_hanging_balls()
    
    def get_adjacent_matches(self, row, col, color, seen):
        if row % 2 == 0:
            neighbors = [(row+1, col-1), (row+1, col), (row, col-1), (row, col+1), (row-1, col-1), (row-1, col)]
        else:
            neighbors = [(row+1, col), (row+1, col+1), (row, col-1), (row, col+1), (row-1, col), (row-1, col+1)]

        matches = []
        for key in neighbors:
            if key not in self.matrix:
                continue
            ball = self.matrix[key]
            if (ball.color == color or color is None) and key not in seen:
                # add match to result and recursive call
                matches.append((key, ball))
                seen.add(key)
                matches.extend(self.get_adjacent_matches(key[0], key[1], color, seen))

        return matches
    
    def add_ball_miss(self, ball):
        x, y = ball.rect.center
        row, col = self.get_nearest_free_space(x, y)
        self.matrix[(row, col)] = ball
        self.group.add(ball)
        ball.rect.center = self.center_points[(row, col)]
        ball.movement = pg.math.Vector2(0, 0)

    def get_nearest_free_space(self, x, y):
        nearest = None
        min_distance = 1E6
        for key, value in self.center_points.items():
            if key not in self.matrix:
                distance = pg.math.Vector2(x, y).distance_to(pg.math.Vector2(value))
                if distance < min_distance:
                    nearest = key
                    min_distance = distance
        return nearest

    def collide(self, ball):
        collision_params = ball.rect.collidedict(self.rects, True)
        if collision_params:
            x, y = ball.rect.center
            row, col = self.get_nearest_free_space(x, y)
            self.add_ball_hit(ball, row, col)
            return True
        return False

    def delete_hanging_balls(self):
        starting_points = filter(lambda t: t[0] == 0, self.matrix)

        not_hanging = set()
        for row, col in starting_points:
            not_hanging.add((row, col))
            for elem in map(lambda t: t[0], self.get_adjacent_matches(row, col, None, {(row, col)})):
                    not_hanging.add(elem)
            
        
        items = list(self.matrix.items())
        for key, ball in items:
            if key not in not_hanging:
                del self.matrix[key]
                self.group.remove(ball)
            
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

    ball_grid = BallGrid()

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
            collision_occured = ball_grid.collide(ball)
            if collision_occured:
                balls.remove(ball)
            elif ball.rect.top <= MARGIN:
                ball_grid.add_ball_miss(ball)
                balls.remove(ball)
            

        # Render graphics here
        #---------------------
        screen.blit(background, (0, 0))
        balls.draw(screen)
        playersprites.draw(screen)
        ball_grid.group.draw(screen)
        clock.tick(60)
        pg.display.flip()


if __name__ == "__main__":
    main()