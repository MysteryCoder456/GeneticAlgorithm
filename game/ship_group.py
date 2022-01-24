import pygame


class ShipGroup(pygame.sprite.Group):
    def update_dna(self):
        for sprite in self:
            sprite.update_dna()

    def render(self, win: pygame.Surface):
        for sprite in self:
            sprite.render(win)
