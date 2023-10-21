from abc import ABCMeta, abstractmethod

class PieceTypes:

    KING = 'king'
    QUEEN = 'queen'
    ROOK = 'rook'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    PAWN = 'pawn'


class Figure(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, color, pos, board):
        self.color = color
        self.pos = pos
        self.is_onboard = True
        self.type = None

    @abstractmethod
    def check_move(self, pos):
        pass

    @abstractmethod
    def make_move(self, pos):
        pass


class King(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.KING

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass


class Queen(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.QUEEN

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass


class Rook(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.ROOK

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass


class Bishop(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.BISHOP

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass


class Knight(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.KNIGHT

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass


class Pawn(Figure):

    def __init__(self, color, pos, board):
        super().__init__(color, pos, board)
        self.type = PieceTypes.PAWN

    def check_move(self, pos):
        pass

    def make_move(self, pos):
        pass
