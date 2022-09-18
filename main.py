import pygame
import sys
import random
from playfield import Playfield
from players import HumanPlayer, MachinePlayer
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dots')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.playfield = Playfield()

        # 0 is player, 1 is enemy
        self.turn = random.randint(0, 1)
        self.turn_count = 0

        self.player = MachinePlayer('Player', 1, self.playfield.map)

        # Comment this line if you want Bot vs BOt game
        self.player = HumanPlayer('Player', 1, self.playfield.map, self.playfield.tile_group)
        self.enemy = MachinePlayer('Enemy', 2, self.playfield.map)
        self.player.assign_opponent(self.enemy)
        self.enemy.assign_opponent(self.player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_over():
                print('\nTurn', self.turn_count)
                if self.turn:
                    turn_owner = self.enemy
                    self.turn = 0
                else:
                    turn_owner = self.player
                    self.turn = 1

                x = y = None

                if type(turn_owner).__name__ == 'HumanPlayer':
                    move_received = False
                    while not move_received:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                try:
                                    x, y = turn_owner.select_move(event.pos)
                                    move_received = True
                                except TypeError:
                                    pass
                else:
                    x, y = turn_owner.select_move(self.turn_count)

                for tile in self.playfield.tile_group:
                    if tile.map_pos == (x, y):
                        tile.fill_tile(turn_owner.dot_color)
                self.playfield.tile_group.draw(self.screen)
                self.turn_count += 1
            else:
                if self.turn:
                    winner = self.player.name
                else:
                    winner = self.enemy.name
                print('\nGame Over!\n', winner, 'is winner')

            pygame.display.update()
            self.clock.tick(FPS)

    def game_over(self):
        str_rows = []
        last_x_index = len(self.playfield.map[0]) - 1
        last_y_index = len(self.playfield.map) - 1

        # Check if 5 in horizontal
        for row in self.playfield.map:
            str_row = ''.join([str(item) for item in row])
            if '11111' in str_row or '22222' in str_row:
                return True
            str_rows.append(str_row)

        # Check if 5 in increasing diagonal
        # Move diagonal to the right
        for k in range(len(self.playfield.map[0])):
            s = ''
            for i in range(len(self.playfield.map)):
                x = i + k
                y = i
                if 0 <= x <= last_x_index and 0 <= y <= last_y_index:
                    s += str(self.playfield.map[-y][x])
            if '11111' in s or '22222' in s:
                return True
        # Move diagonal up
        for k in range(1, len(self.playfield.map)):
            s = ''
            for i in range(len(self.playfield.map)):
                x = i
                y = i + k
                if 0 <= x <= last_x_index and 0 <= y <= last_y_index:
                    s += str(self.playfield.map[-y][x])
            if '11111' in s or '22222' in s:
                return True

        # Check if 5 in decreasing diagonal
        # Move diagonal to the right
        for k in range(len(self.playfield.map[0])):
            s = ''
            for i in range(len(self.playfield.map)):
                x = i + k
                y = i
                if 0 <= x <= last_x_index and 0 <= y <= last_y_index:
                    s += str(self.playfield.map[y][x])
            if '11111' in s or '22222' in s:
                return True
        # Move diagonal down
        for k in range(1, len(self.playfield.map)):
            s = ''
            for i in range(len(self.playfield.map)):
                x = i
                y = i + k
                if 0 <= x <= last_x_index and 0 <= y <= last_y_index:
                    s += str(self.playfield.map[y][x])
            if '11111' in s or '22222' in s:
                return True

        # Check if 5 in vertical
        for i in range(len(str_rows[0])):
            str_col = ''
            for str_row in str_rows:
                str_col += str_row[i]
            if '11111' in str_col or '22222' in str_col:
                return True

        return False


if __name__ == "__main__":
    game = Game()
    restart = game.run()
