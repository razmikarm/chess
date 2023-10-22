from abc import ABCMeta, abstractmethod, abstractstaticmethod
from .utils import Validator, COLOR_NAMES


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

    @abstractstaticmethod
    def possible_moves(curr_pos):
        pass

    def available_moves(self, curr_pos, board):
        """Returns all available positions to move as generator"""
        possible_moves = self.possible_moves(curr_pos)
        for pos in possible_moves:
            row, col = pos
            figure = board[row][col]
            if figure and figure.color == self.color:
                continue
            if self.check_move(curr_pos, pos, board):
                yield pos

    def make_move(self, curr_pos, new_pos, board):
        board = [row.copy() for row in board]
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        board[new_row][new_column] = self
        board[curr_row][curr_column] = None
        return board

    def __str__(self):
        return f"{COLOR_NAMES[self.color]} {self.type}"

    def __repr__(self):
        return f"{COLOR_NAMES[self.color]} {self.type}"


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
        board = self.make_move(curr_pos, new_pos, board)
        return self.check_for_check(self.color, board)

    @staticmethod
    def possible_moves(curr_pos):
        curr_row, curr_column = curr_pos
        up = [(curr_row - 1, curr_column + i) for i in range(-1, 2)]
        curr = [(curr_row, curr_column + i) for i in range(-1, 2)]
        down = [(curr_row + 1, curr_column + i) for i in range(-1, 2)]
        moves = up + down + curr
        return [pos for pos in moves if Validator.is_valid_pos(pos)]

    @staticmethod
    def collect_board_data(color, board):
        my_figures = {}
        opponent_figures = {}
        my_king_pos = opp_king_pos = None
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if isinstance(figure, King) and figure.color == color:
                    my_king_pos = (i, j)
                elif isinstance(figure, King) and figure.color != color:
                        opp_king_pos = (i, j)
                elif figure and figure.color == color:
                    my_figures[(i, j)] = figure
                elif figure:
                    opponent_figures[(i, j)] = figure
        return {
            'my_figures': my_figures,
            'my_king_pos': my_king_pos,
            'opp_king_pos': opp_king_pos,
            'opponent_figures': opponent_figures,
        }

    @staticmethod
    def check_for_check(color, board, cache=None) -> bool:
        return True
        if cache is None:
            cache = King.collect_board_data(color, board)
        
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
    def possible_moves(curr_pos):
        moves = Rook.possible_moves(curr_pos)
        moves += Bishop.possible_moves(curr_pos)
        return moves

    def check_move(self, curr_pos, new_pos, board):
        like_rook = Rook.is_valid_move(curr_pos, new_pos)
        like_bishop = Bishop.is_valid_move(curr_pos, new_pos)
        if not (like_rook or like_bishop):
            return False
        if like_rook:
            cells = Rook.get_cells_btw(curr_pos, new_pos, board)
        else:
            cells = Bishop.get_cells_btw(curr_pos, new_pos, board)
        if any(cells):
            return False
        board = self.make_move(curr_pos, new_pos, board)
        return King.check_for_check(self.color, board)


class Rook(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.ROOK

    @staticmethod
    def possible_moves(curr_pos):
        curr_row, curr_column = curr_pos
        moves = [(i, curr_column) for i in range(8)]
        moves += [(curr_row, i) for i in range(8)]
        return moves

    @staticmethod
    def get_cells_btw(curr_pos, new_pos, board):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        if curr_column == new_column:
            test_board = list(zip(*board))
            curr, new = curr_row, new_row
            row = curr_column
        else:
            test_board = board
            curr, new = curr_column, new_column
            row = curr_row
        if curr < new:
            low, high = curr, new
        else:
            low, high = new, curr
        return test_board[row][low + 1:high]

    @staticmethod
    def is_valid_move(curr_pos, new_pos):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        same_column = curr_column == new_column
        same_row = curr_row == new_row
        return same_column or same_row

    def check_move(self, curr_pos, new_pos, board):
        if not self.is_valid_move(curr_pos, new_pos):
            return False
        if any(self.get_cells_btw(curr_pos, new_pos, board)):
            return False
        board = self.make_move(curr_pos, new_pos, board)
        return King.check_for_check(self.color, board)


class Bishop(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.BISHOP

    @staticmethod
    def possible_moves(curr_pos):
        curr_row, curr_column = curr_pos
        asc_column_start = curr_column - curr_row
        desc_column_start = curr_column + curr_row
        moves = []
        for row in range(8):
            if row == curr_row:
                continue
            asc_pos = asc_column_start + row, row
            desc_pos = asc_column_start - row, row
            if Validator.is_valid_pos(asc_pos):
                moves.append(asc_pos)
            if Validator.is_valid_pos(desc_pos):
                moves.append(desc_pos)
        return moves

    @staticmethod
    def get_cells_btw(curr_pos, new_pos, board):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        # Row icrementing index
        rii = (-1) ** (curr_row > new_row)
        # Column icrementing index
        cii = (-1) ** (curr_column > new_column)
        result = []
        for i in range(1, abs(curr_row - new_row)):
            col = curr_column + i * cii
            row = curr_row + i * rii
            result.append(board[row][col])
        return result

    @staticmethod
    def is_valid_move(curr_pos, new_pos):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        col_diff = abs(curr_column - new_column)
        row_diff = abs(curr_row - new_row)
        return col_diff == row_diff

    def check_move(self, curr_pos, new_pos, board):
        if not self.is_valid_move(curr_pos, new_pos):
            return False
        if any(self.get_cells_btw(curr_pos, new_pos, board)):
            return False
        board = self.make_move(curr_pos, new_pos, board)
        return King.check_for_check(self.color, board)


class Knight(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.KNIGHT

    @staticmethod
    def possible_moves(curr_pos):
        curr_row, curr_column = curr_pos
        up = [(curr_row + 2, curr_column - 1), (curr_row + 2, curr_column + 1)]
        down = [(curr_row - 2, curr_column - 1), (curr_row - 2, curr_column + 1)]
        left = [(curr_row - 1, curr_column - 2), (curr_row + 1, curr_column - 2)]
        right = [(curr_row - 1, curr_column + 2), (curr_row + 1, curr_column + 2)]
        moves = up + down + left + right
        return [pos for pos in moves if Validator.is_valid_pos(pos)]

    def check_move(self, curr_pos, new_pos, board):
        if new_pos not in self.possible_moves(curr_pos):
            return False
        board = self.make_move(curr_pos, new_pos, board)
        return King.check_for_check(self.color, board)


class Pawn(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.type = PieceTypes.PAWN

    @staticmethod
    def possible_moves(curr_pos):
        pass

    def check_move(self, curr_pos, new_pos, board):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        
        board = self.make_move(curr_pos, new_pos, board)
        return King.check_for_check(self.color, board)

ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
PAWNS = [Pawn] * 8

TEXT_FIGURES = {
    1: {
        Rook: "♖",
        Knight: "♘",
        Bishop: "♗",
        King: "♔",
        Queen: "♕",
        Pawn: "♙",
    },
    0: {
        Rook: "♜",
        Knight: "♞",
        Bishop: "♝",
        King: "♚",
        Queen: "♛",
        Pawn: "♟︎",
    },
}
