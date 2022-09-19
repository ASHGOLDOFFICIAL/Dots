import random
import pygame
import sys


class TurnHandler:
    def __init__(self, tile_group, player1, player2):
        self.display_surf = pygame.display.get_surface()
        self.tile_group = tile_group

        if random.randint(0, 1):
            self.player1 = player1
            self.player2 = player2
        else:
            self.player1 = player2
            self.player2 = player1

        self.turn_count = 1

    def turn(self):
        print('\nTurn', self.turn_count)

        # If turn is odd, then turn owner is player 1, otherwise it is player 2
        if self.turn_count % 2:
            turn_owner = self.player1
        else:
            turn_owner = self.player2

        x = y = None

        # If turn owner is human player, then it should wait for user's correct input
        if type(turn_owner).__name__ == 'HumanPlayer':
            move_received = False
            while not move_received:
                for event in pygame.event.get():

                    # Check if user want to exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Check if user clicked his left mouse button
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        try:
                            x, y = turn_owner.select_move(event.pos)
                            move_received = True
                        except TypeError:
                            pass

        # If turn owner is bot, then just let it select tile
        else:
            x, y = turn_owner.select_move()

        for tile in self.tile_group:
            if tile.map_pos == (x, y):
                tile.fill_tile(turn_owner.dot_color)
        self.tile_group.draw(self.display_surf)

        self.turn_count += 1
