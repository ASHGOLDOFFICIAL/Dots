import pygame
from settings import *
from tile import Tile


class Playfield:
    square_size = TILE_SIZE - LINE_WIDTH
    start_pos = (SCREEN_WIDTH // 8, square_size // 2)

    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.map = []
        self.tile_group = pygame.sprite.Group()
        rows, cols = self.draw()
        self.make_map(rows, cols)
        self.make_tiles()

    def draw(self):
        surface = pygame.Surface(pygame.display.get_surface().get_size())

        red_color = (165, 100, 140)
        blue_color = (160, 200, 215)

        rows = cols = 0
        pos_x, pos_y = self.start_pos
        pos_x += self.square_size

        # Draw white background
        surface.fill((250, 255, 255))

        # Draw horizontal lines
        while pos_y < SCREEN_HEIGHT:
            # self.map.append([])
            rows += 1
            pygame.draw.line(surface, blue_color, [0, pos_y], [SCREEN_WIDTH, pos_y], LINE_WIDTH)
            pos_y += self.square_size

        # Draw vertical lines
        while pos_x < SCREEN_WIDTH:
            # for i in range(len(self.map)):
            #     self.map[i].append(0)
            cols += 1
            pygame.draw.line(surface, blue_color, [pos_x, 0], [pos_x, SCREEN_HEIGHT], LINE_WIDTH)
            pos_x += self.square_size

        # Draw red vertical line
        pygame.draw.line(surface, red_color, [self.start_pos[0], 0], [self.start_pos[0], SCREEN_HEIGHT], LINE_WIDTH)

        self.display_surf.blit(surface, (0, 0))
        pygame.display.update()

        return rows, cols

    def make_map(self, rows, cols):
        for i in range(rows):
            self.map.append([])
            for j in range(cols):
                self.map[i].append(0)

    def make_tiles(self):
        for y, row in enumerate(self.map):
            for x in range(len(row)):
                pos_x = (x + 1) * self.square_size + self.start_pos[0] - TILE_SIZE // 3
                pos_y = y * self.square_size + self.start_pos[1] - TILE_SIZE // 3
                pos = (pos_x, pos_y)
                Tile((x, y), pos, DOT_RADIUS * 2.5).add(self.tile_group)
