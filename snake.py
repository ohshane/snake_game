import sys
import random
import pygame
from pygame.constants import K_LEFT
from pygame.cursors import arrow
from pygame.math import Vector2


# x, y coordinates start from the upper left
UP    = Vector2( 0, -1)
RIGHT = Vector2( 1,  0)
DOWN  = Vector2( 0,  1)
LEFT  = Vector2(-1,  0)
STAY  = Vector2( 0,  0)

SPEED = 5

class Color:
    BACKGROUND_FILL   = (127, 215,  70)
    GRASS_FILL        = (167, 209,  61)
    WALL_FILL         = (  0,   0,   0)
    APPLE_FILL        = (200,   0,   0)
    SNAKE_HEAD_BORDER = (  0,   0,   0)
    SNAKE_BODY_BORDER = (  0,   0, 255)
    SNAKE_FILL        = (  0, 100, 255)

class Size:
    BLOCK_SIZE = 20
    SNAKE_BORDER_SIZE = 4

class SnakeGame:

    class _Snake:
        def __init__(self, head, *, length=3, direction=RIGHT):
            if head.x < length or head.y < length:
                raise ValueError
            self.length = length
            self.direction = direction
            self.footprint = [head + (STAY - direction)*i for i in range(length)]

        @property
        def head(self):
            return self.footprint[0]

        @property
        def body(self):
            return self.footprint[0:self.length]

        @property
        def trajectory(self):
            return self.footprint[:-self.length]

        def move(self, direction):
            if self.direction + direction == STAY:
                pass
            else:
                self.direction = direction
                self.footprint.insert(0, self.head + direction)

        def change_length(self, length):
            if length > 2:
                raise ValueError
            self.length += length

    def __init__(self, *, size=(32, 24), speed=SPEED, debug=False):
        self.debug = debug
        self.board = Vector2(size)
        self.speed = speed
        self.snake = SnakeGame._Snake(self.board // 2)
        self.obstacle = {
            'wall' : [],
            'apple': [],
        }
        self.score = 0
        self.game_over = False
        self.__screen = pygame.display.set_mode(list(map(int, self.board * Size.BLOCK_SIZE)))
        self.__clock = pygame.time.Clock()

        self.obstacle['wall'] = self.generate_wall()
        self.obstacle['apple'] = self.generate_apple()

    def generate_wall(self):
        wall = []
        wall.extend([Vector2(i, -1) for i in range(int(self.board.x))])
        wall.extend([Vector2(i, self.board.y) for i in range(int(self.board.x))])
        wall.extend([Vector2(-1, i) for i in range(int(self.board.y))])
        wall.extend([Vector2(self.board.x, i) for i in range(int(self.board.y))])
        return wall

    def generate_apple(self):
        apple = (random.randint(0, self.board.x - 1), random.randint(0, self.board.y - 1))
        if apple in self.snake.body:
            self.generate_apple()
        else:
            return [Vector2(apple)]

    def is_contact(self, obstacle):
        if not isinstance(obstacle, (tuple, list)):
            obstacle = [obstacle]
        return self.snake.head in obstacle

    def is_game_over(self):
        if self.is_contact(self.obstacle['wall']):
            return True
        if self.snake.head in self.snake.body[1:]:
            return True
        return False

    def render(self):
        self.render_background()
        self.render_wall()
        self.render_snake()
        self.render_apple()
        pygame.display.update()

    def render_snake(self):
        for p in self.snake.body:
            if p == self.snake.head:
                pygame.draw.rect(self.__screen,
                                 Color.SNAKE_HEAD_BORDER,
                                 pygame.Rect(p.x * Size.BLOCK_SIZE,
                                             p.y * Size.BLOCK_SIZE,
                                             Size.BLOCK_SIZE,
                                             Size.BLOCK_SIZE))
            else:
                pygame.draw.rect(self.__screen,
                                 Color.SNAKE_BODY_BORDER,
                                 pygame.Rect(p.x * Size.BLOCK_SIZE,
                                             p.y * Size.BLOCK_SIZE,
                                             Size.BLOCK_SIZE,
                                             Size.BLOCK_SIZE))
            pygame.draw.rect(self.__screen,
                             Color.SNAKE_HEAD_BORDER,
                             pygame.Rect(p.x * Size.BLOCK_SIZE + Size.SNAKE_BORDER_SIZE,
                                         p.y * Size.BLOCK_SIZE + Size.SNAKE_BORDER_SIZE,
                                         Size.BLOCK_SIZE - 2 * Size.SNAKE_BORDER_SIZE,
                                         Size.BLOCK_SIZE - 2 * Size.SNAKE_BORDER_SIZE))

    def render_apple(self):
        for p in self.obstacle['apple']:
            pygame.draw.rect(self.__screen,
                             Color.APPLE_FILL,
                             pygame.Rect(p.x * Size.BLOCK_SIZE,
                                         p.y * Size.BLOCK_SIZE,
                                         Size.BLOCK_SIZE,
                                         Size.BLOCK_SIZE))

    def render_wall(self):
        for p in self.obstacle['wall']:
            pygame.draw.rect(self.__screen,
                             Color.WALL_FILL,
                             pygame.Rect(p.x * Size.BLOCK_SIZE,
                                         p.y * Size.BLOCK_SIZE,
                                         Size.BLOCK_SIZE,
                                         Size.BLOCK_SIZE))

    def render_background(self):
        self.__screen.fill(Color.BACKGROUND_FILL)
        for x in range(int(self.board.x)):
            for y in range(int(self.board.y)):
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                    pygame.draw.rect(self.__screen,
                                     Color.GRASS_FILL,
                                     pygame.Rect(x * Size.BLOCK_SIZE,
                                                 y * Size.BLOCK_SIZE,
                                                 Size.BLOCK_SIZE,
                                                 Size.BLOCK_SIZE))


    def play_scene(self):
        if self.debug and self.game_over:
            import time
            time.sleep(0.5)
            self.snake.__init__(self.board // 2)
            self.game_over = False
            self.score = 0

        events = pygame.event.get()
        arrow_keydown = False
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if not arrow_keydown and event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]:
                        arrow = None
                        if event.key == pygame.K_UP:
                            arrow = UP
                        elif event.key == pygame.K_RIGHT:
                            arrow = RIGHT
                        elif event.key == pygame.K_DOWN:
                            arrow = DOWN
                        elif event.key == pygame.K_LEFT:
                            arrow = LEFT
                        if self.snake.direction == arrow or (self.snake.direction + arrow) == STAY:
                            arrow_keydown = self.snake.direction
                            self.snake.move(self.snake.direction)
                        else:
                            arrow_keydown = arrow
                            self.snake.move(arrow)
        else:
            self.snake.move(self.snake.direction)
        
        if self.is_game_over():
            self.game_over = True
            self.snake.move(STAY)

        if self.is_contact(self.obstacle['apple']):
            self.obstacle['apple'] = self.generate_apple()
            self.snake.change_length(1)
            self.score += 1

        self.render()
        self.__clock.tick(self.speed)

        return self.game_over, self.score


if __name__ == '__main__':
    import math
    count = 0
    debug = True
    game = SnakeGame(speed=math.inf, debug=debug)
    while True:
        count += 1
        game_over, score = game.play_scene()
        print(count, game_over, score)
        if game_over:
            print(f"score: {score}")
            count = 0
            if not debug:
                break