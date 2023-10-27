from abc import ABCMeta, abstractmethod
from utils import Validator, Colors


class PieceNames:

    KING = ('K', 'King')
    ROOK = ('R', 'Rook')
    PAWN = ('P', 'Pawn')
    QUEEN = ('Q', 'Queen')
    BISHOP = ('B', 'Bishop')
    KNIGHT = ('N', 'Knight')


class Figure(metaclass=ABCMeta): # TODO: Implement Singleton for colors

    @abstractmethod
    def __init__(self, color):
        self.color = color
        self.name = None
        self.notation = None

    @staticmethod
    @abstractmethod
    def possible_moves(curr_pos, color=None):
        pass

    @abstractmethod
    def is_available_move(self, curr_pos, new_pos, board):
        pass

    def can_move(self, curr_pos, new_pos, board):
        new_row, new_column = new_pos
        figure = board[new_row][new_column]
        if figure is not None and self.color == figure.color:
            return False
        if not self.is_available_move(curr_pos, new_pos, board):
            return False
        board = self.make_move(curr_pos, new_pos, board)
        return Figure.is_not_check(self.color, board)

    def make_move(self, curr_pos, new_pos, board):
        board = [row.copy() for row in board]
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos
        board[new_row][new_column] = self
        board[curr_row][curr_column] = None
        return board

    @staticmethod
    def collect_board_data(color, board):
        my_figures = {}
        opponent_figures = {}
        my_king_pos = opp_king_pos = None
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if figure is not None:
                    if isinstance(figure, King):
                        if figure.color == color:
                            my_king_pos = (i, j)
                        else:
                            opp_king_pos = (i, j)
                    elif figure.color == color:
                        my_figures[(i, j)] = figure
                    else:
                        opponent_figures[(i, j)] = figure
        return {
            'my_figures': my_figures,
            'my_king_pos': my_king_pos,
            'opp_king_pos': opp_king_pos,
            'opponent_figures': opponent_figures,
        }

    @staticmethod
    def is_not_check(color, board, cache=None) -> bool:
        if cache is None:
            cache = Figure.collect_board_data(color, board)

        my_king_pos = cache['my_king_pos']
        opp_king_pos = cache['opp_king_pos']
        opponent_figures = cache['opponent_figures']

        if (abs(my_king_pos[0] - opp_king_pos[0]) <= 1 and
                abs(my_king_pos[1] - opp_king_pos[1]) <= 1):
                return False
        for pos, figure in opponent_figures.items():
            if figure.is_available_move(pos, my_king_pos, board):
                return False
        return True

    @staticmethod
    def check_for_mate(color, board):
        
        data = Figure.collect_board_data(color, board)
        
        my_figures = data['my_figures']
        my_king_pos = data['my_king_pos']

        if Figure.is_not_check(color, board, cache=data):
            return

        my_king = board[my_king_pos[0]][my_king_pos[1]]
        for pos in my_king.possible_moves(my_king_pos, color):
            if my_king.can_move(my_king_pos, pos, board):
                return

        for curr_pos, figure in my_figures.items():
            for pos in figure.possible_moves(curr_pos, color):
                if figure.can_move(curr_pos, pos, board):
                    return

        return color


class King(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.KING[1]
        self.notation = PieceNames.KING[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        curr_row, curr_column = curr_pos
        up = [(curr_row - 1, curr_column + i) for i in range(-1, 2)]
        curr = [(curr_row, curr_column + i) for i in range(-1, 2)]
        down = [(curr_row + 1, curr_column + i) for i in range(-1, 2)]
        moves = up + curr + down
        return [pos for pos in moves if Validator.is_valid_pos(pos)]

    def is_available_move(self, curr_pos, new_pos, board):
        curr_row, curr_column = curr_pos
        new_row, new_column = new_pos

        return (abs(curr_row - new_row) <= 1 and
            abs(curr_column - new_column) <= 1)


class Queen(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.QUEEN[1]
        self.notation = PieceNames.QUEEN[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        moves = Rook.possible_moves(curr_pos, color)
        moves += Bishop.possible_moves(curr_pos, color)
        return moves

    def is_available_move(self, curr_pos, new_pos, board):
        like_rook = Rook.is_valid_move(curr_pos, new_pos)
        like_bishop = Bishop.is_valid_move(curr_pos, new_pos)
        if not (like_rook or like_bishop):
            return False
        if like_rook:
            cells = Rook.get_cells_btw(curr_pos, new_pos, board)
        else:
            cells = Bishop.get_cells_btw(curr_pos, new_pos, board)
        return not any(cells)


class Rook(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.ROOK[1]
        self.notation = PieceNames.ROOK[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        curr_row, curr_column = curr_pos
        moves = [(i, curr_column) for i in range(8) if i != curr_row]
        moves += [(curr_row, i) for i in range(8) if i != curr_column]
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

    def is_available_move(self, curr_pos, new_pos, board):
        if not self.is_valid_move(curr_pos, new_pos):
            return False
        return not any(self.get_cells_btw(curr_pos, new_pos, board))


class Bishop(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.BISHOP[1]
        self.notation = PieceNames.BISHOP[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        curr_row, curr_column = curr_pos
        asc_column_start = curr_column - curr_row
        desc_column_start = curr_column + curr_row
        moves = []
        for row in range(8):
            if row == curr_row:
                continue
            asc_pos = asc_column_start + row, row
            desc_pos = desc_column_start - row, row
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

    def is_available_move(self, curr_pos, new_pos, board):
        if not self.is_valid_move(curr_pos, new_pos):
            return False
        return not any(self.get_cells_btw(curr_pos, new_pos, board))


class Knight(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.KNIGHT[1]
        self.notation = PieceNames.KNIGHT[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        curr_row, curr_column = curr_pos
        up = [(curr_row + 2, curr_column - 1), (curr_row + 2, curr_column + 1)]
        down = [(curr_row - 2, curr_column - 1), (curr_row - 2, curr_column + 1)]
        left = [(curr_row - 1, curr_column - 2), (curr_row + 1, curr_column - 2)]
        right = [(curr_row - 1, curr_column + 2), (curr_row + 1, curr_column + 2)]
        moves = up + down + left + right
        return [pos for pos in moves if Validator.is_valid_pos(pos)]

    def is_available_move(self, curr_pos, new_pos, board):
        return new_pos in self.possible_moves(curr_pos, self.color)


class Pawn(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.name = PieceNames.PAWN[1]
        self.notation = PieceNames.PAWN[0]

    @staticmethod
    def possible_moves(curr_pos, color=None):
        if color is None:
            return []
        curr_row, curr_column = curr_pos
        is_new_black = color == 1 and curr_row == 1
        is_new_white = color == 0 and curr_row == 6
        moves = [
            (curr_row - (-1) ** color, curr_column),
            (curr_row - (-1) ** color, curr_column - 1),
            (curr_row - (-1) ** color, curr_column + 1),
        ]
        if is_new_black or is_new_white:
            moves.append((curr_row - (2 * (-1) ** color), curr_column))
        # TODO: Need to add checker for `en passant`
        return [pos for pos in moves if Validator.is_valid_pos(pos)]

    def is_available_move(self, curr_pos, new_pos, board):
        _, curr_column = curr_pos
        possibles = self.possible_moves(curr_pos, self.color)
        acceptables = []
        for p in possibles:
            if ((board[p[0]][p[1]] is not None and p[1] != curr_column) or
                (board[p[0]][p[1]] is None and p[1] == curr_column)):
                acceptables.append(p)
        return new_pos in acceptables


ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
PAWNS = [Pawn] * 8

TEXT_FIGURES = {
    Colors.BLACK: {
        Rook: "♖",
        Knight: "♘",
        Bishop: "♗",
        King: "♔",
        Queen: "♕",
        Pawn: "♙",
    },
    Colors.WHITE: {
        Rook: "♜",
        Knight: "♞",
        Bishop: "♝",
        King: "♚",
        Queen: "♛",
        Pawn: "♟︎",
    },
}
