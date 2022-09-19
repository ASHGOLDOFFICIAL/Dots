import random
from combination_priority import CombinationPriority


class Player:
    def __init__(self, name, dot_num, playfield_map):
        self.playfield_map = playfield_map
        self.last_move = None
        self.name = name
        self.dot_num = dot_num
        if self.dot_num == 1:
            self.dot_color = 0
        else:
            self.dot_color = 1

    def assign_opponent(self, opponent):
        self.opponent = opponent


class HumanPlayer(Player):
    def __init__(self, name, dot_num, playfield_map, tile_group):
        super().__init__(name, dot_num, playfield_map)
        self.tile_group = tile_group
    
    def select_move(self, pos):
        for tile in self.tile_group:
            if tile.rect.collidepoint(pos) and not self.playfield_map[tile.map_pos[1]][tile.map_pos[0]]:
                x, y = tile.map_pos[0], tile.map_pos[1]
                self.playfield_map[y][x] = self.dot_num
                self.last_move = (x, y)
                print(self.name + "'s move is", self.last_move)
                return x, y


class MachinePlayer(Player):
    combination_priority = CombinationPriority()
    
    def __init__(self, name, dot_num, playfield_map):
        super().__init__(name, dot_num, playfield_map)
        self.playfield_map = playfield_map
        self.last_x_index = len(playfield_map[0]) - 1
        self.last_y_index = len(playfield_map) - 1

        if self.dot_num == 1:
            self.opponent_dot_num = 2
        else:
            self.opponent_dot_num = 1
        self.dots = []

    def select_move(self):
        if not self.opponent.last_move:
            x, y = self.select_random_tile()
        else:
            self.dots.append(self.opponent.last_move)
            self.dots.sort()
            x, y = self.analyze()
        self.last_move = (x, y)
        self.dots.append(self.last_move)
        self.dots.sort()
        self.playfield_map[y][x] = self.dot_num
        print(self.name + "'s move is", self.last_move)
        return x, y

    def analyze(self):
        # Create dict of best moves with 10 priority levels
        best_moves = {}
        for i in range(10):
            best_moves[str(i)] = []

        for dot in self.dots:
            self.check_neighbours(dot[0], dot[1], best_moves)

        for priority in range(len(best_moves)):
            priority = str(priority)

            if best_moves[priority]:
                print(self.name, 'selects best move')
                # print(best_moves[priority])
                return best_moves[priority][random.randrange(len(best_moves[priority]))]

        print(self.name, 'selects random tile')
        return self.select_random_tile()

    def check_neighbours(self, x, y, moves_dict):
        orig_x, orig_y = x, y
        for direction_x in -1, 0, 1:
            for direction_y in -1, 0, 1:
                x, y = orig_x, orig_y
                # If they both are 0, then x and y won't change and make combinations
                if direction_x == 0 and direction_y == 0:
                    continue

                combination = ''
                for k in range(5):
                    x += k * direction_x
                    y += k * direction_y
                    combination += self.get_tile_value(x, y)

                # If combination doesn't contain an empty tile, then there's no place for dot
                if '0' not in combination:
                    continue

                for priority in range(len(moves_dict)):
                    priority = str(priority)
                    if combination in self.combination_priority[priority]:
                        empty_tiles_indexes = []
                        while combination.count('0'):
                            empty_tiles_indexes.append(combination.index('0'))
                            combination = combination.replace('0', 'r', 1)
                        for i in empty_tiles_indexes:
                            moves_dict[priority] += [(orig_x + i * direction_x, orig_y + i * direction_y)]

                    # Remove all moves which are out of playfield
                    moves_dict[priority] = list(filter(
                        lambda move: 0 <= move[0] <= self.last_x_index and
                                     0 <= move[1] <= self.last_y_index and
                                     self.playfield_map[move[1]][move[0]] == 0,
                        moves_dict[priority]))

    def get_tile_value(self, x, y):
        if 0 <= x <= self.last_x_index and 0 <= y <= self.last_y_index:
            if self.playfield_map[y][x] == self.opponent_dot_num:
                # 'o' for 'opponent'
                return 'o'
            elif self.playfield_map[y][x] == self.dot_num:
                # 'p' for 'player', meaning this MachinePlayer
                return 'p'
            else:
                # '0' for empty tile
                return '0'
        else:
            # 'e' for 'error', meaning value is out of range
            return 'e'

    def select_random_tile(self):
        while True:
            tiles_all = len(self.playfield_map) * len(self.playfield_map[0])
            if len(self.dots) == tiles_all:
                break

            y = random.randint(0, len(self.playfield_map) - 1)
            x = random.randint(0, len(self.playfield_map[0]) - 1)
            if not self.playfield_map[y][x]:
                return x, y
