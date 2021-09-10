import sys
from collections import namedtuple
import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

pygame.display.set_caption('Snake game')

SPEED = 5
BLOCK_SIZE = 20

p = namedtuple('x', 'y')
p.x = 320
p.y = 240

move_key = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                move_key = event.key

    if move_key == pygame.K_UP:
        p.y -= BLOCK_SIZE
    elif move_key == pygame.K_DOWN:
        p.y += BLOCK_SIZE
    elif move_key == pygame.K_LEFT:
        p.x -= BLOCK_SIZE
    elif move_key == pygame.K_RIGHT:
        p.x += BLOCK_SIZE

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(p.x, p.y, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.update()

    clock.tick(SPEED)