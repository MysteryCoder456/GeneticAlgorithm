import random
import pygame
from pygame import Vector2
from game.ship import Ship, DNA_LENGTH


class ShipGroup(pygame.sprite.Group):
    def __init__(self, *ships: Ship, starting_pos: Vector2, target: Vector2):
        super().__init__(*ships)
        self.starting_pos = starting_pos
        self.target = target
        self.gene_pool: list[list] = []
        self.fitness_threshold = 4000000
        self.mutation_scale = 5
        self.generation_number = 1
        random.seed()

    def gather_dna(self):
        for ship in self:
            ship_pos: Vector2 = ship.pos  # just for type hinting
            fitness = round(
                self.fitness_threshold
                / ship_pos.distance_squared_to(self.target)
            )
            for _ in range(fitness):
                self.gene_pool.append(ship.dna)

    def spawn_next_generation(self, ship_count: int):
        self.empty()

        for _ in range(ship_count):
            parent1_dna = random.choice(self.gene_pool)
            parent2_dna = random.choice(self.gene_pool)

            haploid_dna_size = DNA_LENGTH // 2
            new_dna = (
                parent1_dna[:haploid_dna_size] + parent2_dna[haploid_dna_size:]
            )

            for dna_piece in new_dna:
                dna_piece += (random.random() * 2 - 1) * self.mutation_scale

            new_ship = Ship(self.starting_pos.copy(), new_dna)
            self.add(new_ship)

        self.gene_pool = []
        self.generation_number += 1

    def update_dna(self):
        for sprite in self:
            sprite.update_dna()

    def render(self, win: pygame.Surface):
        for sprite in self:
            sprite.render(win)
