from game_of_life_constants import *


"""
class Board:
    def __init__(self, board: [[bool]]):
        self.board = board
        self.x_size = len(board[0])
        self.y_size = len(board)
        self.dim = self.x_size, self.y_size

    def __or__(self, other):
        if self.dim != other.dim:
            raise DimentionError
        return Board(
            [[self.board[i][j] or other.board[i][j] for j in range(self.x_size)] for i in range(self.y_size)])

"""


class Game:
    game = None

    """def __new__(cls, *args, **kwargs):
        if cls.game is not None:
            return cls.game
        return super().__new__(cls)"""

    def __init__(self, board: [[]]):
        Game.game = self
        self.board = board
        self.x_size = len(board[0])
        self.y_size = len(board)
        self.z_size = 0
        self.dim = self.x_size, self.y_size

    def update_board(self):
        old_board = self.board
        # new_board = old_board
        new_board = []
        for y in range(self.y_size):
            new_board.append([])
            for x in range(self.x_size):
                alive_cells_around_xy = self.num_alive_cells_around(x, y)
                # new_board[y][x] = self.life_or_death(self.board[y][x], alive_cells_around_xy)
                new_board[-1].append(
                    self.life_or_death(old_board[y][x], alive_cells_around_xy)
                )
        self.board = new_board

    def life_or_death(self, state, n_cells):
        # à implémenter
        pass

    def num_alive_cells_around(self, x, y, z=None):
        sum_result = 0
        if z is None:
            for i, j in [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or 0 != j]:
                sum_result += self.board[(y+i) % self.y_size][(x+j) % self.x_size]
            return sum_result

        for i, j in [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1) if i != 0 or 0 != j or k != 0]:
            sum_result += self.board[(z + i) % self.z_size][(y + i) % self.y_size][(x + j) % self.x_size]
        return sum_result


class Game3D(Game):
    def __init__(self, board: [[[]]]):
        super(Game3D, self).__init__(board)
        self.z_size, self.y_size, self.x_size = len(board), len(board[0]), len(board[0][0])
        self.dim = self.x_size, self.y_size, self.z_size

    def update_board(self):
        old_board = self.board
        # new_board = old_board
        new_board = []
        for z in range(self.z_size):
            new_board.append([])
            for y in range(self.y_size):
                new_board[-1].append([])
                for x in range(self.x_size):
                    alive_cells_around_xyz = self.num_alive_cells_around(x, y, z)
                    # new_board[y][x] = self.life_or_death(self.board[y][x], alive_cells_around_xy)
                    new_board[-1][-1].append(
                        self.life_or_death(old_board[z][y][x], alive_cells_around_xyz)
                    )
        self.board = new_board

    def num_alive_cells_around(self, x, y, z=None):
        if z is None:
            sum_result = 0
            for i, j in [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or 0 != j]:
                sum_result += self.board[(y+i) % self.y_size][(x+j) % self.x_size]
            return sum_result
        else:
            sum_result = 0
            for i, j, k in [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1) if any((i, j, k))]:
                sum_result += self.board[(z + k) % self.x_size][(y + i) % self.y_size][(x + j) % self.x_size]
            return sum_result


class ConwayGameOfLife(Game):
    def __init__(self, board: [[bool]]):
        super().__init__(board)

    def int_board(self):
        return [[int(i) for i in j] for j in self.board]

    def life_or_death(self, alive, n_cells) -> bool:
        if alive:
            return 2 <= n_cells <= 3
        else:
            return 3 == n_cells

    # def lives_or_dies(self, x, y):
    #     alive = self.board[y][x]
    #     n_cells = self.num_alive_cells_around(x, y)
    #     if self.life_or_death(alive, n_cells):
    #         return "l"
    #     return "d"
    #
    # def __repr__(self):
    #     res = "__" * self.x_size + "\n"
    #
    #     for line in self.board:
    #         for x in line:
    #             if x:
    #                 res += "<>"
    #             else:
    #                 res += ".."
    #         res += "\n"
    #     return res + "__" * self.x_size
    #
    # """def print_neighbours_number(self):  # for debugging
    #     res = "__" * self.x_size + "\n"
    #
    #     for y in range(self.y_size):
    #         for x in range(self.x_size):
    #             alive_cells_around_xy = self.num_alive_cells_around(x, y)
    #
    #             if self.board[y][x]:
    #                 res += self.lives_or_dies(x, y) + f"@{alive_cells_around_xy}|"
    #             else:
    #                 res += self.lives_or_dies(x, y) + f" {alive_cells_around_xy}|"
    #         res += "\n"
    #     print(res)"""

    def display(self, window=WIN, dark_theme=DARK_THEME):
        for y in range(self.y_size):
            for x in range(self.x_size):
                cell_im = dead_im(dark_theme)
                if self.board[y][x]:
                    cell_im = alive_im(dark_theme)
                window.blit(cell_im, (x * CELL_SPACING + TOP_LEFT_x, y * CELL_SPACING + TOP_LEFT_y))

    def change_cell(self, mouse_position):
        pos_x, pos_y = mouse_position
        pos_x -= TOP_LEFT_x
        pos_y -= TOP_LEFT_y
        x = pos_x // CELL_SPACING
        y = pos_y // CELL_SPACING
        if x <= self.x_size and y <= self.y_size:
            self.board[y][x] = not self.board[y][x]

    def __or__(self, other):
        x_size = max(self.x_size, other.x_size)
        y_size = max(self.y_size, other.y_size)
        self.change_dimentions((x_size, y_size))
        other.change_dimentions((x_size, y_size))
        return ConwayGameOfLife(
            [[self.board[y][x] or other.board[y][x] for x in range(x_size)] for y in range(y_size)]
        )

    def change_dimentions(self, dimentions: tuple):
        x_size, y_size = dimentions
        if self.x_size >= x_size:
            self.board = self.board[:][:x_size]
        else:
            for _ in range(x_size - self.x_size):
                for i in range(self.y_size):
                    self.board[i].append(False)
        if self.y_size >= y_size:
            self.board = self.board[:][:y_size]
        else:
            for _ in range(y_size - self.y_size):
                self.board.append([0 for _ in range(x_size)])
        self.dim = self.x_size, self.y_size = x_size, y_size


class Button:
    def __init__(self, top_left: int, bottom_right: int, function, image):
        self.top_left, self.bottom_right = top_left, bottom_right
        self.function = function
        self.image = image


if __name__ == '__main__':
    def main():
        from time import sleep

        # print(*[(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or 0 != j])
        # print("bonjour")
        # print("bonjour")
        game = ConwayGameOfLife([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]])
        for _ in range(40):
            print(game)
            game.update_board()
            sleep(1/4)

    main()
