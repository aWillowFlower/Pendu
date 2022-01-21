import pygame
import os
from mymath import DimensionError

# WIDTH, HEIGHT = 1280, 700
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode()


# directions
UP = (0, -1)
DOWN = (0, 1)  # the positive y direction is pointing down
RIGHT = (1, 0)
LEFT = (-1, 0)

# rgb
BLANC = (255, 255, 255)
GRIS = (127, 127, 127)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
JAUNE = (0, 255, 255)
ROSE = (255, 0, 255)
colors = (BLANC, GRIS, NOIR, ROUGE, BLEU, VERT, JAUNE, ROSE)

FPS = 60
DELTA_T = 1 / FPS
TOP_LEFT_x, TOP_LEFT_y = 15, 10


CELL_SIZE = 20  # 33 cells sur 18 cells
CELL_SPACING = round(CELL_SIZE * 1.1)


def color_square(color: str, size: int = CELL_SIZE):
    image = pygame.image.load(os.path.join("Assets", color + " square.png")).convert()
    return pygame.transform.scale(image, (size, size))


ALL_COLORS = ("Black", "Blue", "Green", "Red", "White", "Orange", "Yellow")


BLACK_SQUARE = pygame.image.load(os.path.join("Assets", "Black square.png"))
BLACK_IM = pygame.transform.scale(BLACK_SQUARE, (CELL_SIZE, CELL_SIZE))
WHITE_SQUARE = pygame.image.load(os.path.join("Assets", "White square.png"))
WHITE_IM = pygame.transform.scale(WHITE_SQUARE, (CELL_SIZE, CELL_SIZE))

DARK_THEME: bool = False

ALIVE_IM = BLACK_IM
DEAD_IM = WHITE_IM
if DARK_THEME:
    ALIVE_IM = WHITE_IM
    DEAD_IM = BLACK_IM


def dead_im(dark_theme=DARK_THEME):
    if dark_theme:
        return BLACK_IM
    return WHITE_IM


def alive_im(dark_theme=DARK_THEME):
    if dark_theme:
        return WHITE_IM
    return BLACK_IM


def background_color(dark_theme=DARK_THEME):
    if dark_theme:
        return NOIR
    return BLANC


class YouTube:
    def __init__(self, window: type(WIN) = WIN, initial_speed: float = 0.2, fps: float = 60, dark_theme: bool = False):
        self.clock: type(pygame.time.Clock()) = pygame.time.Clock()
        self.running: bool = True
        self.playing: bool = True

        self.window: type(WIN) = window
        self.initial_speed: float = initial_speed
        self.speed: float = initial_speed
        self.fps: float = fps
        self.dark_theme: bool = dark_theme

        self.prev_keys = pygame.key.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.new_keys = pygame.key.get_pressed()

    def get_keys(self):
        keys = pygame.key.get_pressed()

        self.prev_keys = self.keys
        self.keys = keys
        self.new_keys = {key: item for key, item in enumerate(keys)}
        return keys, self.new_keys

    def handle_keys(self, keys, new_keys):
        if new_keys[pygame.K_SPACE]:
            self.playing = True
        if new_keys[pygame.K_n]:
            self.dark_theme = not self.dark_theme

    def handle_playing_keys(self, keys, new_keys):
        self.handle_keys(keys, new_keys)

        if keys[pygame.K_COMMA]:
            self.speed *= 1.1
        if keys[pygame.K_COLON]:
            self.speed /= 1.1
        if keys[pygame.K_MINUS]:
            self.speed = self.initial_speed

    def handle_pause_keys(self, keys, new_keys):
        self.handle_keys(keys, new_keys)


class Play:
    def __init__(self, game):
        self.youtube: YouTube = game.youtube
        self.game = game

    def create(self):
        self.youtube.window.fill(BLANC)
        self.game.display()
        self.youtube.keys = pygame.key.get_pressed()

    def loop(self):
        while self.youtube.running:
            while self.youtube.playing:
                # playing loop
                self.youtube.clock.tick(int(FPS * self.youtube.speed))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.youtube.running, self.youtube.playing = False, False

                    self.game.handle_playing_event(event)

                keys, new_keys = self.youtube.get_keys()

                self.youtube.handle_playing_keys(keys, new_keys)
                self.game.handle_playing_keys(keys, new_keys)

                self.game.display_updated()
                self.game.update_board()

            self.youtube.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.youtube.running, self.youtube.playing = False, False

                self.game.handle_pause_event(event)

            keys, new_keys = self.youtube.get_keys()

            self.youtube.handle_pause_keys(keys, new_keys)
            self.game.handle_pause_keys(keys, new_keys)

            self.game.display_updated()
            self.game.update_board()


class Screen:
    def __init__(self,
                 board: [[]],
                 type_=None,
                 region_size: int = CELL_SIZE,
                 youtube: YouTube = YouTube(),
                 shift: (int, int) = (0, 0)):

        self.board: list = board
        self.__init_board__(board, type_)
        self.youtube: YouTube = youtube

        self.window: type(WIN) = youtube.window
        self.region_size: int = region_size
        self.dark_theme: bool = youtube.dark_theme
        self.shift = self.shift_x, self.shift_y = shift

    def __init_board__(self, board, type_: type = None):
        """initializes the board part of the Screen"""
        self.previous_board = self.board[:]
        self.board = board
        self.x_size = len(board[0])
        self.y_size = len(board)
        self.dimentions = self.x_size, self.y_size

        if type_ is None:
            self.type = type(board[0][0])
        else:
            self.type = type_

        self.zero = self.type()

        for col in board:
            if len(col) != self.x_size:
                raise DimensionError()
            for value in col:
                if type(value) != self.type:
                    raise TypeError()

    def __getitem__(self, item):
        return self.board[item]

    def __iter__(self):
        return self.board.__iter__()

    def __len__(self):
        return len(self.board)

    def get_value(self, x, y):
        return self[y % len(self)][x % len(self[0])]

    def update_board(self) -> None:
        """updates the board according to the rules \n\n
        to implement in the subclass
        """
        pass

    def region_image(self, value) -> pygame.Surface:
        """
        the image corresponding to the value \n
        :param value: the value at the region
        :return: the image corresponding to the value
        \n\n
        to implement in the subclass
        """
        if self.dark_theme:
            return BLACK_IM
        return WHITE_IM

    def display(self) -> None:
        for y, y_col in enumerate(self):
            for x, value in enumerate(y_col):
                cell_im = self.region_image(value)
                position = (x * self.region_size + self.shift_x, y * self.region_size + self.shift_x)
                self.window.blit(cell_im, position)

    def display_updated(self) -> None:
        for y, (col, prev_col) in enumerate(zip(self.board, self.previous_board)):
            for x, (value, prev_value) in enumerate(zip(col, prev_col)):
                if value != prev_value:
                    cell_im = self.region_image(value)
                    position = (x * self.region_size + self.shift_x, y * self.region_size + self.shift_x)
                    self.window.blit(cell_im, position)

        pygame.display.update()

    def add_lines(self, x: int, up: int):
        board = self.board[:]
        zero = self.zero
        new_board = board[:]
        if up > 0:
            n_lines = up
            new_board = [[zero] * self.x_size] * n_lines + board
        if up < 0:
            n_lines = - up
            new_board = board + [[zero] * self.x_size] * n_lines

        if x > 0:
            n_columns = x
            new_board = [line + [zero for _ in range(n_columns)] for line in new_board]
        if x < 0:
            n_columns = - x
            new_board = [[zero for _ in range(n_columns)] + line for line in new_board]

        self.__init_board__(new_board, self.type)

    def remove_lines(self, x: int, up: int):
        new_board = self.board
        if x > 0:
            new_board = [line[:len(line) - x] for line in self.board]
        if x < 0:
            new_board = [line[- x:] for line in self.board]

        if up > 0:
            new_board = self.board[:len(new_board) - up]
        if up < 0:
            new_board = self.board[-up:]

        self.__init_board__(new_board, self.type)

    def pixel_to_region(self, x, y):
        return (x - self.shift_x) // self.region_size, (y - self.shift_y) // self.region_size

