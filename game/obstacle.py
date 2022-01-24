import pathlib
import pygame
from pygame import Vector2

SPRITE_PATH = pathlib.Path(__file__).parent / "assets" / "obstacle.png"


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, scale: float):
        self.pos = position

        sprite_image = pygame.image.load(SPRITE_PATH)
        original_size = Vector2(sprite_image.get_size())
        self.image = pygame.transform.smoothscale(
            sprite_image, original_size * scale
        )
        self.rect = self.image.get_rect()

        super().__init__()

    def render(self, win: pygame.Surface):
        draw_pos = self.pos - (Vector2(self.image.get_size()) / 2)
        win.blit(self.image, draw_pos)
