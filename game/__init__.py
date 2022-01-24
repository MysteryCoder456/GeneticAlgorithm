from random import randint, random
import pygame
from pygame import Vector2
from pygame.sprite import Sprite

from game.ship import Ship, DNA_LENGTH
from game.ship_group import ShipGroup
from game.obstacle import Obstacle

WIN_SIZE = Vector2(1204, 820)
FPS = 60
GENERATION_SIZE = 20
GENERATION_TIME = 15  # sec
START_POSITION = Vector2(50, 50)
TARGET = Vector2(WIN_SIZE.x - 50, WIN_SIZE.y - 50)

UPDATE_VELOCITY_EVENT = pygame.USEREVENT + 1
NEXT_GENERATION_EVENT = pygame.USEREVENT + 2


def collision_callback(sprite1: Sprite, sprite2: Sprite) -> bool:
    rect1 = sprite1.image.get_rect()
    rect2 = sprite2.image.get_rect()

    radius1 = Vector2(max(rect1[2], rect1[3])).magnitude() / 2
    radius2 = Vector2(max(rect2[2], rect2[3])).magnitude() / 2

    center_pos1 = sprite1.pos - Vector2(rect1[2], rect1[3]) / 2
    center_pos2 = sprite2.pos - Vector2(rect2[2], rect2[3]) / 2

    return center_pos1.distance_to(center_pos2) <= radius1 + radius2


def main():
    pygame.init()

    win = pygame.display.set_mode((WIN_SIZE.x, WIN_SIZE.y))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Genetic Algo Demo", "???")

    ship_group = ShipGroup(
        *[Ship(START_POSITION.copy()) for _ in range(GENERATION_SIZE)],
        starting_pos=START_POSITION,
        target=TARGET,
    )
    obstacle_group = pygame.sprite.Group(
        *[
            Obstacle(
                Vector2(
                    randint(100, WIN_SIZE.x - 100),
                    randint(100, WIN_SIZE.y - 150),
                ),
                random() + 0.5,
            )
            for _ in range(randint(5, 7))
        ]
    )

    vel_update_interval = int(GENERATION_TIME / DNA_LENGTH * 1000)  # ms
    pygame.time.set_timer(UPDATE_VELOCITY_EVENT, vel_update_interval)
    pygame.time.set_timer(NEXT_GENERATION_EVENT, GENERATION_TIME * 1000)

    arial_font = pygame.font.SysFont("Arial", 30)

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
        pygame.sprite.groupcollide(
            ship_group, obstacle_group, True, False, collision_callback
        )

        win.fill(pygame.Color("gray"))

        ship_group.render(win)

        for obstacle in obstacle_group:
            obstacle.render(win)

        pygame.draw.circle(win, pygame.Color("red"), TARGET, 20)

        generation_text = arial_font.render(
            f"Gen {ship_group.generation_number}",
            False,
            pygame.Color("white"),
            pygame.Color("black"),
        )
        win.blit(generation_text, (20, WIN_SIZE.y - 50))

        pygame.display.flip()
