from abc import ABCMeta, abstractmethod

class PieceTypes:

    KING = 'king'
    QUEEN = 'queen'
    ROOK = 'rook'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    PAWN = 'pawn'


class Figure(metaclass=ABCMeta): # TODO: Implement Singleton for colors

    @abstractmethod
    def __init__(self, color):
        self.color = color
        self.type = None

    @abstractmethod
    def check_move(self, curr_pos, new_pos, board):
        pass

    def __str__(self):
        return f"{self.color} {self.type}"

    def __repr__(self):
        return f"{self.color} {self.type}"


class King(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.KING

    def check_move(self, curr_pos, new_pos, board):
        pass


class Queen(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.QUEEN

    def check_move(self, curr_pos, new_pos, board):
        pass


class Rook(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.ROOK

    def check_move(self, curr_pos, new_pos, board):
        pass


class Bishop(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.BISHOP

    def check_move(self, curr_pos, new_pos, board):
        pass


class Knight(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.KNIGHT

    def check_move(self, curr_pos, new_pos, board):
        pass


class Pawn(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.PAWN

    def check_move(self, curr_pos, new_pos, board):
        pass

LEFT_SIDE = [Rook, Knight, Bishop]
RIGHT_SIDE = LEFT_SIDE[::-1]

WHITES_ORDER = LEFT_SIDE + [Queen, King] + RIGHT_SIDE
BLACKS_ORDER = LEFT_SIDE + [King, Queen] + RIGHT_SIDE
PAWNS = [Pawn] * 8
