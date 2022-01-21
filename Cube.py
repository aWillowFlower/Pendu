from typing import Union
from GameOfLife.game_of_life_constants import *
from mymath import *


class Face(Vector3):
    def __init__(self, x: Union[int, float, Vector3] = 0, y=0, z=0, color: int = None):
        super(Face, self).__init__(x, y, z)
        if color is None:
            self.reset_color()
        else:
            self.color: int = color

    def set_color(self, color):
        self.color = color

    def reset_color(self):
        done = False
        for i, (comp, ) in enumerate(self):
            if comp > 0 and not done:
                self.color = 2 * i
                done = True
            if comp < 0 and not done:
                self.color = 2 * i + 1
                done = True
        if not done:
            self.color: int = 0

    def __repr__(self):
        return super(Face, self).__repr__()[:-1] + f", {self.color})"


class Piece:
    def __init__(self, position: Vector3, *faces: Face):
        self.position: Vector3 = position
        self.faces: [Face] = list(faces)

    def apply_matrix(self, matrix: Matrix):
        if matrix.dim != (3, 3):
            raise ValueError
        self.position = matrix * self.position
        for i, face in enumerate(self.faces[:]):
            self.faces[i] = Face(matrix * face, color=face.color)


def decompose_vec(vec: Vector3) -> [Vector3]:
    res: [Vector3] = []
    for i, (comp, ) in enumerate(vec):
        if comp > 0:
            res.append(Vector3(*[int(i == j) for j in range(3)]))
        if comp < 0:
            res.append(Vector3(*[-int(i == j) for j in range(3)]))
    return res


def decompose_face(vec: Vector3) -> [Face]:
    vectors = decompose_vec(vec)
    return [Face(vector) for vector in vectors]


class RubicksCube:
    def __init__(self):
        # self.corners = []
        # self.edges = []
        # self.centers = [Piece(m * Vector3(*vec), Face(m * Vector3(*vec)))
        #                 for m in (-1, 1) for vec in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]

        self.pieces: [Piece] = [
            Piece(Vector3(i, j, k), *decompose_face(Vector3(i, j, k)))
            for i in range(-1, 2) for j in range(-1, 2) for k in range(-1, 2)
            if (i, j, k) != (0, 0, 0)
        ]

    def rotate(self, matrix: Matrix):
        if matrix.dim != (3, 3):
            raise ValueError()
        for piece in self.pieces:
            piece.apply_matrix(matrix)

    def up(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_yx)

    def uup(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_yx * R_yx)

    def upp(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_xy)

    def right(self):
        for piece in self.pieces:
            if piece.position.y > 0:
                piece.apply_matrix(R_xz)

    def rright(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_xz * R_xz)

    def rightp(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_zx)

    def down(self):
        for piece in self.pieces:
            if piece.position.z < 0:
                piece.apply_matrix(R_xy)

    def ddown(self):
        for piece in self.pieces:
            if piece.position.z < 0:
                piece.apply_matrix(R_xy * R_xy)

    def downp(self):
        for piece in self.pieces:
            if piece.position.z < 0:
                piece.apply_matrix(R_yx)

    def left(self):
        for piece in self.pieces:
            if piece.position.y < 0:
                piece.apply_matrix(R_zx)

    def lleft(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_zx * R_zx)

    def leftp(self):
        for piece in self.pieces:
            if piece.position.z > 0:
                piece.apply_matrix(R_xz)

    def front(self):
        for piece in self.pieces:
            if piece.position.x > 0:
                piece.apply_matrix(R_zy)

    def ffront(self):
        for piece in self.pieces:
            if piece.position.x > 0:
                piece.apply_matrix(R_zy * R_zy)

    def frontp(self):
        for piece in self.pieces:
            if piece.position.x > 0:
                piece.apply_matrix(R_yz)

    def back(self):
        for piece in self.pieces:
            if piece.position.x < 0:
                piece.apply_matrix(R_yz)

    def bback(self):
        for piece in self.pieces:
            if piece.position.x < 0:
                piece.apply_matrix(R_yz * R_yz)

    def backp(self):
        for piece in self.pieces:
            if piece.position.x < 0:
                piece.apply_matrix(R_zy)


class RubickScreen(Screen):
    def __init__(self, board: [[int]], cube: RubicksCube = RubicksCube(), youtube: YouTube = YouTube(), **kwargs):
        super(RubickScreen, self).__init__(board=board, type_=int, youtube=youtube, **kwargs)

        self.cube: RubicksCube = cube


if __name__ == '__main__':
    def main():
        cube = RubicksCube()
        cube.uup()
        i = 0
        for piece in cube.pieces:
            for face in piece.faces:
                if e1 in decompose_vec(face):
                    i += 1
                    # print(repr(piece.position), repr(face), i)
                    print(repr(face))

    main()
