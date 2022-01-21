from spaceships import *
from Screen import *


def game_of_life_loop(game):
    dark_theme: bool = False

    def draw_window():
        WIN.fill(background_color(dark_theme))
        game.display(WIN, dark_theme)
        pygame.display.update()

    clock = pygame.time.Clock()
    running = True
    playing = True
    speed = 0.02
    while running:
        while playing:
            clock.tick(FPS * speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running, playing = False, False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            keys = pygame.key.get_pressed()

            if keys[pygame.K_c]:
                if keys[pygame.K_SPACE]:
                    playing = False
            if keys[pygame.K_UP]:
                speed *= 1.1
            if keys[pygame.K_DOWN]:
                speed /= 1.1
            if keys[pygame.K_d]:
                dark_theme = False
            if keys[pygame.K_n]:
                dark_theme = True

            draw_window()
            game.update_board()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, playing = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.change_cell(pygame.mouse.get_pos())

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_c]:
            if keys[pygame.K_p]:
                playing = True
        if keys[pygame.K_d]:
            dark_theme = False
        if keys[pygame.K_n]:
            dark_theme = True
        if keys[pygame.K_t]:
            print("[", end="")
            print(*[str(line) + ",\n" for line in game.int_board()], end="")
            print("")
        draw_window()


def spline_loop(game: SplinesScreen, initial_speed: float = 0.2):
    dark_theme: bool = False

    clock = pygame.time.Clock()
    running: bool = True
    playing: bool = True
    speed: float = initial_speed
    prev_keys = pygame.key.get_pressed()

    WIN.fill(background_color(dark_theme))
    game.display()

    while running:
        while playing:
            clock.tick(FPS * speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running, playing = False, False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print(pygame.mouse.get_pos())
                    if not game.points:
                        game.add_point(Point(
                            *game.pixel_to_region(*pygame.mouse.get_pos())))
                        game.selected_point = game.points[0]
                        game.selected_index = 0
                    else:
                        game.add_point(Point(
                            *game.pixel_to_region(*pygame.mouse.get_pos())))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
                playing = False
            if keys[pygame.K_n] and not prev_keys[pygame.K_n]:
                dark_theme = not dark_theme

            if keys[pygame.K_COMMA]:
                speed *= 1.1
            if keys[pygame.K_COLON]:
                speed /= 1.1
            if keys[pygame.K_MINUS]:
                speed = initial_speed

            if keys[pygame.K_UP]:
                game.move_selected_point(0, -1)
            if keys[pygame.K_DOWN]:
                game.move_selected_point(0, 1)
            if keys[pygame.K_RIGHT]:
                game.move_selected_point(1, 0)
            if keys[pygame.K_LEFT]:
                game.move_selected_point(-1, 0)

            if keys[pygame.K_TAB] and not prev_keys[pygame.K_TAB]:
                game.change_point(True)
            if keys[pygame.K_DELETE] and not prev_keys[pygame.K_DELETE]:
                game.change_point(False)

            prev_keys = keys

            game.display_updated()
            game.update_board()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, playing = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.add_point(Point(
                    *game.pixel_to_region(*pygame.mouse.get_pos())))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
            playing = True
        if keys[pygame.K_n] and not prev_keys[pygame.K_n]:
            dark_theme = not dark_theme

        if keys[pygame.K_UP]:
            game.move_selected_point(0, -1)
        if keys[pygame.K_DOWN]:
            game.move_selected_point(0, 1)
        if keys[pygame.K_RIGHT]:
            game.move_selected_point(1, 0)
        if keys[pygame.K_LEFT]:
            game.move_selected_point(-1, 0)

        prev_keys = keys
        game.display_updated()


def main():
    """function to call to play"""
    """game = ConwayGameOfLife([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])"""
    game = CANON
    game.change_dimentions((56, 30))
    print(game.dim)
    game_of_life_loop(game)


def spline():
    resolution = 3
    # initial_points = [Point(i, 15) for i in range(10, 41, 10)]
    initial_points = []
    game = SplinesScreen([[0]*56 * round(resolution)]*30 * round(resolution),
                         initial_points,
                         region_size=CELL_SIZE // resolution)
    spline_loop(game, initial_speed=0.5)


def oospline():
    resolution = 3
    initial_points = []
    game = SplinesScreen([[0]*56 * round(resolution)]*30 * round(resolution),
                         initial_points,
                         region_size=CELL_SIZE // resolution)
    play = Play(game)
    play.create()
    play.loop()


if __name__ == "__main__":
    oospline()
