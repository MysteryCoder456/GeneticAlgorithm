import glm
import pygame

WIN_SIZE = (720, 720)
FPS = 60
win = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Genetic Algo Demo", "???")


def main():
    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        win.fill(pygame.Color("black"))

        pygame.draw.rect(win, pygame.Color("white"), (10, 10, 100, 100))

        pygame.display.flip()
