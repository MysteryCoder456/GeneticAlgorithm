import pygame
from pygame.math import Vector2

from game.ship import Ship, DNA_LENGTH
from game.ship_group import ShipGroup

WIN_SIZE = Vector2(1204, 820)
FPS = 60
GENERATION_SIZE = 20
GENERATION_TIME = 15  # sec
START_POSITION = Vector2(150, WIN_SIZE.y - 150)

UPDATE_VEL_EVENT = pygame.USEREVENT + 1


def main():
    pygame.init()

    win = pygame.display.set_mode((WIN_SIZE.x, WIN_SIZE.y))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Genetic Algo Demo", "???")

    ship_group = ShipGroup(
        *[Ship(START_POSITION.copy()) for _ in range(GENERATION_SIZE)]
    )
    vel_update_interval = int(GENERATION_TIME / DNA_LENGTH * 1000)  # ms
    pygame.time.set_timer(UPDATE_VEL_EVENT, vel_update_interval)

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == UPDATE_VEL_EVENT:
                ship_group.update_dna()

        ship_group.update(dt)

        win.fill(pygame.Color("gray"))

        ship_group.render(win)

        pygame.display.flip()
