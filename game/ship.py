import pathlib
from random import random
import pygame
from pygame.math import Vector2

DNA_LENGTH = 250
SPRITE_PATH = pathlib.Path(__file__).parent / "assets" / "ship.png"


class Ship(pygame.sprite.Sprite):
    def __init__(self, start_pos: Vector2, dna: list[float] = []):
        self.pos = start_pos
        self.vel = Vector2()
        self.speed: float = 100
        self.turn_speed: float = 10

        self.dna = self.form_dna(dna)
        self.current_dna_index = 0
        self.angle = self.get_current_dna()

        self.image = pygame.image.load(SPRITE_PATH)
        super().__init__()

    def form_dna(self, dna: list[Vector2]) -> list[float]:
        dna_list = dna

        while len(dna_list) < DNA_LENGTH:
            dna_piece = (random() * 2 - 1) * self.turn_speed
            dna_list.append(dna_piece)

        while len(dna_list) > DNA_LENGTH:
            dna_list.pop(-1)

        return dna_list

    def get_current_dna(self) -> float:
        return self.dna[self.current_dna_index]

    def update_dna(self):
        self.current_dna_index = min(
            self.current_dna_index + 1, DNA_LENGTH - 1
        )
        self.angle = self.get_current_dna()

    def update(self, dt: float):
        self.vel.from_polar((self.speed, self.angle))
        self.pos += self.vel * dt

    def render(self, win: pygame.Surface):
        rotated_image = pygame.transform.rotate(
            self.image, (self.angle + 90) * -1
        )
        win.blit(rotated_image, self.pos)