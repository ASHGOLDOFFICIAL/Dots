import pygame
# from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, map_pos, pos, size):
        super().__init__()
        self.map_pos = map_pos

        self.image = pygame.Surface((size, size))

        # Make sprite transparent
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect(topleft=pos)

    def fill_tile(self, dot_color):
        size = self.image.get_width() // 2
        if dot_color == 0:
            pygame.draw.circle(self.image, (10, 10, 55), (size, size), size)
        else:
            pygame.draw.circle(self.image, (10, 10, 55), (size, size), size, size // 3)
