class DimensionError(ValueError):
    pass


def mot(matrix: [[]], str_or_repr=str):
    f = str_or_repr
    max_len = 0
    for col in matrix:
        for value in col:
            if max_len < len(f(value)):
                max_len = len(f(value))

    res = "["
    for x, col in enumerate(matrix):
        if x != 0:
            res += ",\n "

        res += "["
        for y, value in enumerate(col):
            word = f(value)
            if y != 0:
                res += "," + (1 - len(word) + max_len) * " "
            res += word
        res += "]"
    res += "]"
    return res


class Matrix:

    def __init__(self, matrix_list: [[float]]):
        self.matrix_list: [[float]]

        if isinstance(matrix_list, (list, tuple)):
            # base case where matrix lis is a list or a tuple
            self.matrix_list: [[float]] = list(matrix_list)
            if not matrix_list:
                raise ValueError()
            self.dim = len(matrix_list), len(matrix_list[0])
        elif isinstance(matrix_list, Matrix):
            # to create a matrix witch is the same as the given one
            self.matrix_list: [[float]] = matrix_list.matrix_list
            self.dim = matrix_list.dim
        else:
            raise TypeError()

        size = len(matrix_list[0])
        # check if all the columns have the same length
        for col in self.matrix_list:
            if len(col) != size:
                raise DimensionError()

    def __getitem__(self, item):
        return self.matrix_list[item]

    def __setitem__(self, key, value):
        self.matrix_list[key] = value

    def __iter__(self):
        return self.matrix_list

    def T(self):
        """the transposed matrix"""
        res_list = [[self.matrix_list[y][x] for x in range(self.dim[0])] for y in range(self.dim[1])]
        return type(self)(res_list)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # scale by a scalar
            return type(self)([[other * el for el in line] for line in self])
        is_matrix = isinstance(other, Matrix)

        other = to_matrix(other)
        res = []
        dim = self.dim[0], other.dim[1]
        if self.dim[1] != other.dim[0]:
            raise ValueError()
        for line in range(dim[0]):
            res.append([])
            for col in range(dim[1]):
                res[-1].append(sum([self[line][i] * other[i][col] for i in range(self.dim[1])]))

        if is_matrix:
            return type(other)(res)
        return type(self)(res)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return type(self)([[other * el for el in line] for line in self])
        other = to_matrix(other)
        return other * self

    def __add__(self, other):
        if self.dim != other.dim:
            raise ValueError()
        return type(self)([[se + ot for se, ot in zip(se_row, ot_row)] for se_row, ot_row in zip(self, other)])

    def __neg__(self):
        return type(self)([[- el for el in line] for line in self])

    def __sub__(self, other):
        return self + other.__neg__()

    def __eq__(self, other):
        return self.matrix_list == other.matrix_list

    def __repr__(self):
        return type(self).__name__ + "(" + repr(self.matrix_list)[1:-1] + ")"

    def __str__(self):
        return mot(self)

    def __pow__(self, power, modulo=None):
        if self.dim[0] != self.dim[1]:
            raise ValueError()
        if power == 0:
            return identity(self.dim[0])
        return self * self.__pow__(power, modulo)


def identity(dim: int) -> Matrix:
    return Matrix([[int(i == j) for i in range(dim)] for j in range(dim)])


def to_matrix(mat) -> Matrix:
    if isinstance(mat, (int, float)):
        return Matrix([[mat]])
    if isinstance(mat, Matrix):
        return mat
    if isinstance(mat, (list, tuple)):
        return Matrix(mat)
    raise TypeError


class Vector(Matrix):
    def __init__(self, *components):
        if len(components) == 1 and isinstance(components[0], (list, tuple, Matrix)):
            super(Vector, self).__init__([[el[0]] for el in components[0]])
            self.components = tuple([
                el[0] for el in components[0]
                ])
        else:
            for comp in components:
                if not isinstance(comp, (int, float)):
                    raise TypeError
            super(Vector, self).__init__([[component] for component in components])
            self.size: int = len(components)
            self.components = list(components)

    def dot(self, other):
        if self.dim != other.dim:
            raise ValueError
        return sum([el[0] * ot[0] for el, ot in zip(self, other)])

    def __repr__(self):
        return type(self).__name__ + repr(tuple(self.components))


class Vector3(Vector):
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, (list, Matrix, tuple)) and y == 0 == z:
            super(Vector3, self).__init__(x[:3])
            [self.x], [self.y], [self.z] = x[:3]
        else:
            super(Vector3, self).__init__(x, y, z)
            self.x, self.y, self.z = x, y, z

    def cross(self, other):
        return Vector3(self.y * other.z - self.z * other.y,
                       self.x * other.z - self.z * other.x,
                       self.x * other.y - self.y * other.x)

    def perp_in_xy(self):
        return Vector3(-self.y, self.x, self.z)


R_xy = Matrix([[0, -1, 0],
               [1, 0, 0],
               [0, 0, 1]])
R_yx = Matrix([[0, 1, 0],
               [-1, 0, 0],
               [0, 0, 1]])
R_xz = Matrix([[0, 0, -1],
               [0, 1, 0],
               [1, 0, 0]])
R_zx = Matrix([[0, 0, 1],
               [0, 1, 0],
               [-1, 0, 0]])
R_yz = Matrix([[1, 0, 0],
               [0, 0, -1],
               [0, 1, 0]])
R_zy = Matrix([[1, 0, 0],
               [0, 0, 1],
               [0, -1, 0]])

e1 = Vector3(1, 0, 0)
e2 = Vector3(0, 1, 0)
e3 = Vector3(0, 0, 1)


class Set:
    def __init__(self, *elements):
        self.list = []
        for element in elements:
            self.add(element)

    def add(self, new_element):
        for element in self:
            if element != new_element:
                self.list.append(new_element)

    def sub(self, old_element):
        if old_element in self.list:
            self.list.remove(old_element)

    def __getitem__(self, item):
        return self.list[item]

    def __len__(self):
        return len(self.list)

    def __contains__(self, item):
        for el in self.list:
            if el == item and type(el) == type(item):
                return True
        return False

    def __add__(self, other):
        res = Set(*self.list)
        for element in other:
            res.add(element)
        return res

    def __sub__(self, other):
        res = Set(*self.list)
        for element in other:
            res.sub(element)
        return res

    def issubset(self, other) -> bool:
        is_subset = True
        for el in self:
            if el not in other:
                is_subset = False
                break
        return is_subset

    def issuperset(self, other) -> bool:
        issuperset = True
        for el in other:
            if el not in self:
                issuperset = False
                break
        return issuperset

    def __eq__(self, other):
        return self.issubset(other) and other.is_subset(self)
