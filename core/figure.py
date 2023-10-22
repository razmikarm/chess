from abc import ABCMeta, abstractmethod, abstractstaticmethod
from .utils import Validator

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

    @abstractmethod
    def available_moves(self, curr_pos, board):
        pass

    @abstractstaticmethod
    def _possible_moves(curr_pos):
        pass

    def available_moves(self, curr_pos, board):
        """Returns all available positions to move as generator"""
        possible_moves = self._possible_moves(curr_pos)
        for pos in possible_moves:
            if self.check_move(curr_pos, pos, board):
                yield pos

    def __str__(self):
        return f"{self.color} {self.type}"

    def __repr__(self):
        return f"{self.color} {self.type}"


class King(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.KING

    def check_move(self, curr_pos, new_pos, board) -> bool:
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos

        if not (abs(curr_row - new_row) <= 1 and 
                abs(curr_column - new_column) <= 1):
                return False
        baord = [row.copy() for row in board]
        board[new_row][new_column] = self
        board[curr_row][curr_column] = None
        return self.check_for_check(self.color, board)

    @staticmethod
    def _possible_moves(curr_pos):
        curr_row, curr_column = curr_pos
        up = [(curr_row - 1, curr_column + i) for i in range(-1, 2)]
        down = [(curr_row + 1, curr_column + i) for i in range(-1, 2)]
        curr = [(curr_row, curr_column + i) for i in range(-1, 2)]
        return [pos for pos in up + down + curr if Validator.is_valid_pos(pos)]


    @staticmethod
    def collect_board_data(color, board):
        my_figures = {}
        opponent_figures = {}
        my_king_pos = opp_king_pos = None
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if isinstance(figure, King) and figure.color == color:
                    my_king_pos = (i, j)
                elif figure and figure.color == color:
                    my_figures[(i, j)] = figure
                elif figure:
                    if isinstance(figure, King):
                        opp_king_pos = (i, j)
                    else:
                        opponent_figures[(i, j)] = figure
        return {
            'my_figures': my_figures,
            'my_king_pos': my_king_pos,
            'opp_king_pos': opp_king_pos,
            'opponent_figures': opponent_figures,
        }

    @staticmethod
    def check_for_check(color, board, cache=None) -> bool:
        if cache is None:
            cache = self._collect_board_data(color, board)
        
        my_figures = cache['my_figures']
        my_king_pos = cache['my_king_pos']
        opp_king_pos = cache['opp_king_pos']
        opponent_figures = cache['opponent_figures']

        if (abs(my_king_pos[0] - opp_king_pos[0]) <= 1 and 
                abs(my_king_pos[1] - opp_king_pos[1]) <= 1):
                return True
        for pos, figure in opponent_figures.items():
            if figure.check_move(pos, my_king_pos, board):
                return True
        return False

    @staticmethod
    def check_for_mate(color, board):
        
        data = self.collect_board_data(color, board)
        
        my_figures = cache['my_figures']
        my_king_pos = cache['my_king_pos']
        opp_king_pos = cache['opp_king_pos']
        opponent_figures = cache['opponent_figures']

        if not King.check_for_check(color, board, cache=data):
            return False

        my_king = board[my_king_pos[0]][my_king_pos[1]]
        if my_king.available_moves(my_king_pos, board):
            return False
        
        for curr_pos, figure in my_figures.items():
            if figure.available_moves(curr_pos, board):
                return False

        return color



class Queen(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.QUEEN

    @staticmethod
    def _possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        pass


class Rook(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.ROOK

    @staticmethod
    def _possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        pass


class Bishop(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.BISHOP

    @staticmethod
    def _possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        pass


class Knight(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.KNIGHT

    @staticmethod
    def _possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        pass


class Pawn(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.PAWN

    @staticmethod
    def _possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        pass

ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
PAWNS = [Pawn] * 8
