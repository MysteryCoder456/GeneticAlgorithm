import pygame
from pygame import Vector2

from game.ship import Ship, DNA_LENGTH
from game.ship_group import ShipGroup

WIN_SIZE = Vector2(1204, 820)
FPS = 60
GENERATION_SIZE = 20
GENERATION_TIME = 10  # sec
START_POSITION = Vector2(50, 50)
TARGET = Vector2(WIN_SIZE.x - 50, WIN_SIZE.y - 50)

UPDATE_VELOCITY_EVENT = pygame.USEREVENT + 1
NEXT_GENERATION_EVENT = pygame.USEREVENT + 2


def main():
    pygame.init()

    win = pygame.display.set_mode((WIN_SIZE.x, WIN_SIZE.y))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Genetic Algo Demo", "???")

    ship_group = ShipGroup(
        *[Ship(START_POSITION.copy()) for _ in range(GENERATION_SIZE)],
        starting_pos=START_POSITION,
        target=TARGET
    )
    vel_update_interval = int(GENERATION_TIME / DNA_LENGTH * 1000)  # ms
    pygame.time.set_timer(UPDATE_VELOCITY_EVENT, vel_update_interval)
    pygame.time.set_timer(NEXT_GENERATION_EVENT, GENERATION_TIME * 1000)

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == UPDATE_VELOCITY_EVENT:
                ship_group.update_dna()

            if event.type == NEXT_GENERATION_EVENT:
                ship_group.gather_dna()
                ship_group.spawn_next_generation(GENERATION_SIZE)

        ship_group.update(dt)

        win.fill(pygame.Color("gray"))

        ship_group.render(win)
        pygame.draw.circle(win, pygame.Color("red"), TARGET, 20)

        pygame.display.flip()
