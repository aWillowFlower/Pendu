from game_of_life_constants import *
from mymath import *


class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.in_x, self.int_y = self.xy = int(x), int(y)
        self.x: float = x
        self.y: float = y

    def translate(self, x, y):
        self.__init__(self.x + x, self.y + y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Point(other.x + self.x, other.y + self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + other.__neg__()

    def __rsub__(self, other):
        return other + self.__neg__()

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)


def to_int_point(vector: pygame.Vector2):
    return int(vector.x), int(vector.y)


class Particle(Point):
    def __init__(self, x: int = 0, y: int = 0, vx: int = 0, vy: int = 0, radius: float = 1.):
        super(Particle, self).__init__(x, y)
        self.vx, self.vy = vx, vy
        self.radius: float = radius

    def move(self, dt):
        self.translate(self.vx * dt, self.vy * dt)

    def get_squared_distance_to(self, other: "Particle") -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def get_intersection(self, *other_points: "Particle"):
        for other in other_points:
            if self.get_squared_distance_to(other) < (self.radius + other.radius) ** 2:
                return other
        return None


class Bezier:
    def __init__(self, *points: pygame.Vector2):
        self.points: [pygame.Vector2] = list(points)

    def param_func(self, t: float) -> pygame.Vector2:
        first, *points, last = self.points
        if points:
            return (1-t) * Bezier(first, *points).param_func(t) + t * Bezier(*points, last).param_func(t)
        return (1-t) * first + t * last


class Timm:
    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.points: [pygame.Vector2] = list((p1, p2, p3, p4))

    def param_func(self, t: float) -> pygame.Vector2:
        p1, p2, p3, p4 = self.points
        extreme_factor: float = ((2*t-1) ** 2 - 1) / 2
        border_1_fact: float = - t**2 * (1-t)
        border_2_fact: float = - t * (1-t)**2

        middle_factor: float = 3 * t ** 2 - 2 * t ** 3
        # middle_factor = 10 * t**3 - 15 * t ** 4 + 6 * t ** 5
        res: pygame.Vector2 = 2 * (border_1_fact * (p1 - p2) - border_2_fact * (p3 - p4)) \
                              + middle_factor * p2 + (1 - middle_factor) * p3

        return res


class Leo:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points: [pygame.Vector2] = list((p1, p2, p3))

    def param_func(self, t: float) -> pygame.Vector2:
        p1, p2, p3 = self.points
        extreme_factor: float = ((2*t-1) ** 2 - 1) / 2
        border_1_fact: float = - t**2 * (1-t)
        border_2_fact: float = - t * (1-t)**2

        middle_factor: float = 3 * t ** 2 - 2 * t ** 3
        # middle_factor = 10 * t**3 - 15 * t ** 4 + 6 * t ** 5
        res: pygame.Vector2 = 2 * (border_1_fact * (p1 - p2) - border_2_fact * (p2 - p3)) \
                              + middle_factor * p2 + (1 - middle_factor) * p3

        return res


class SplinesScreen(Screen):

    def __init__(self, board: [[int]], points: [Point], youtube: YouTube = YouTube(), **kwargs):
        super(SplinesScreen, self).__init__(board=board, type_=int, youtube=youtube, **kwargs)

        self.points: [Point] = list(points)
        self.selected_index: int
        self.selected_point: Point
        if points:
            self.selected_index: int = 0
            self.selected_point: Point = points[0]

        self.previous_board = [[self.zero for _ in col] for col in self]

        self.value = {"around selected point": 4,
                      "around point": 3,
                      "point": 2,
                      "spline": 1,
                      "empty": 0}
        self.state = {0: "empty",
                      1: "spline",
                      2: "point",
                      3: "around point",
                      4: "around selected point"}
        self.color = {0: color_square("Black", self.region_size),
                      1: color_square("White", self.region_size),
                      2: color_square("Green", self.region_size),
                      3: color_square("Blue", self.region_size),
                      4: color_square("Red", self.region_size)}

    def update_board(self) -> None:
        new_board = [[self.value["empty"] for _ in line] for line in self.board]
        # TODO update the splines
        for spline in self.get_splines():
            t = 0.
            dt = 0.1 / len(self)
            while t <= 1:
                x, y = to_int_point(spline.param_func(t))
                new_board[y % len(new_board)][x % len(new_board[0])] = self.value["spline"]
                t += dt

        # updates the points
        for point in self.points:
            for x in range(-1, 1 + 1):
                for y in range(-1, 1 + 1):
                    px, py = point.xy
                    if x == 0 == y:
                        new_board[(py + y) % len(new_board)][(px + x) % len(new_board[0])]\
                            = self.value["point"]
                    else:
                        new_board[(py + y) % len(new_board)][(px + x) % len(new_board[0])]\
                            = self.value["around point"]

        # updates the selected point
        if self.points:
            sp_x, sp_y = self.selected_point.xy
            new_board[sp_y % len(new_board)][sp_x % len(new_board[0])]\
                = self.value["around selected point"]

        self.__init_board__(new_board, self.type)

    def region_image(self, value) -> pygame.Surface:
        # TODO handle the dark theme
        return self.color[value]

    def change_point(self, is_next: bool = True):
        self.selected_index = (self.selected_index + 2*is_next - 1) % len(self.points)
        self.selected_point = self.points[self.selected_index]

    def move_selected_point(self, *direction):
        self.points[self.selected_index].translate(*direction)
        self.selected_point = self.points[self.selected_index]

    def add_point(self, point: Point):
        self.points.append(point)

    def get_splines(self) -> [Timm]:
        if len(self.points) < 4:
            return []

        res: [Timm] = []
        for i in range(len(self.points) - 3):
            res.append(Timm(*[self.points[i + j] for j in range(4)]))
        return res

    # --------------------------------   to make consistant with the Play class   --------------------------------

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # adds a new point
            if not self.points:
                # if it has no point it has to select it
                self.add_point(Point(
                    *self.pixel_to_region(*pygame.mouse.get_pos())))
                self.selected_point = self.points[0]
                self.selected_index = 0
            else:
                self.add_point(Point(
                    *self.pixel_to_region(*pygame.mouse.get_pos())))

    def handle_playing_event(self, event):
        self.handle_event(event)
        pass

    def handle_pause_event(self, event):
        self.handle_event(event)
        pass

    def handle_keys(self, keys, new_keys):
        if keys[pygame.K_UP]:
            self.move_selected_point(0, -1)
        if keys[pygame.K_DOWN]:
            self.move_selected_point(0, 1)
        if keys[pygame.K_RIGHT]:
            self.move_selected_point(1, 0)
        if keys[pygame.K_LEFT]:
            self.move_selected_point(-1, 0)

    def handle_playing_keys(self, keys, new_keys):
        self.handle_keys(keys, new_keys)

        if new_keys[pygame.K_TAB]:
            self.change_point(True)
        if new_keys[pygame.K_DELETE]:
            self.change_point(False)

    def handle_pause_keys(self, keys, new_keys):
        self.handle_keys(keys, new_keys)
        pass


class Polygon:
    def __init__(self, *points: Vector3):
        self.points: [Vector3] = list(points)

    def __getitem__(self, item):
        return self.points[item % len(self.points)]

    def contains_point(self, point: Vector3):
        if any([point.x == p.x for p in self.points]):
            # TODO handle this case
            pass


