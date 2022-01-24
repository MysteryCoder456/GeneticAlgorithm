import pathlib
from random import randint
import pygame
from pygame.math import Vector2


class Ship(pygame.sprite.Sprite):
    pos: Vector2
    dna: list[Vector2]

    speed: float = 5.0
    current_dna_index = 0

    DNA_LENGTH = 46
    SPRITE_PATH = pathlib.Path(__file__).parent / "assets" / "ship.png"

    def __init__(self, start_pos: Vector2, dna: list = []):
        self.pos = start_pos
        self.image = pygame.image.load(self.SPRITE_PATH)

        self.form_dna(dna)
        super().__init__()

    def form_dna(self, dna: list):
        if dna:
            self.dna = dna

            while len(self.dna) < self.DNA_LENGTH:
                dna_piece = Vector2(
                    randint(-1, 1) * self.speed,
                    randint(-1, 1) * self.speed,
                )
                self.dna.append(dna_piece)

            while len(self.dna) > self.DNA_LENGTH:
                self.dna.pop(-1)

        else:
            self.dna = []
            for _ in range(self.DNA_LENGTH):
                dna_piece = Vector2(
                    randint(-1, 1) * self.speed,
                    randint(-1, 1) * self.speed,
                )
                self.dna.append(dna_piece)

    def get_current_vel(self):
        return self.dna[self.current_dna_index]

    def update(self, dt: float, update_vel: bool = False):
        if update_vel:
            self.current_dna_index += min(1, self.DNA_LENGTH - 1)

        self.pos += self.get_current_vel() * self.speed * dt

    def render(self, win: pygame.Surface):
        angle = self.get_current_vel().as_polar()[1]
        rotated_image = pygame.transform.rotate(self.image, angle)
        win.blit(rotated_image, self.pos)
