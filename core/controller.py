from uuid import uuid4, UUID

from .board import Board
from .utils import Colors

class Controller:

    def __init__(self):
        self.boards = {}
        self._letters = ' ABCDEFGH'

    def make_move(self, board_id, from_cell, to_cell):
        board_id = self.convert_id(board_id)
        if not board_id:
            return
        if not (board := self.boards.get(board_id)):
            return
        if not self.is_valid_cellname(from_cell):
            return
        if not self.is_valid_cellname(to_cell):
            return
        from_pos = self.cellname_to_pos(from_cell)
        to_pos = self.cellname_to_pos(to_cell)
        return board.make_move(from_pos, to_pos)

    def start_new_board(self):
        new_id = uuid4()
        self.boards[new_id] = Board(new_id)
        return new_id

    def end_board(self, board_id):
        board_id = self.convert_id(board_id)
        if not board_id:
            return
        if not self.boards.get(board_id):
            return
        return self.boards.pop(board_id)

    def all_boards(self):
        return list(self.boards.keys())

    def show_board(self, board_id):
        board_id = self.convert_id(board_id)
        if not board_id:
            return
        if not self.boards.get(board_id):
            return
        return self.boards[board_id].state

    def is_valid_cellname(self, cellname):
        if not isinstance(cellname, str):
            return False
        if len(cellname) != 2:
            return False
        if not self.is_valid_column(cellname[0]):
            return False
        if not self.is_valid_row(cellname[1]):
            return False
        return True

    def is_valid_pos(self, pos):
        if not isinstance(pos, (tuple, list)):
            return False
        if len(pos) != 2:
            return False
        if not (0 <= pos[0] <= 7):
            return False
        if not (0 <= pos[1] <= 7):
            return False
        return True

    def is_valid_row(self, row):
        if not isinstance(row, (int, str)):
            return False
        if isinstance(row, str):
            if not (len(row) == 1 and row.isdigit()):
                return False
            row = int(row)
        if not (0 < row < 9):
            return False
        return True

    def is_valid_column(self, column):
        if not isinstance(column, (int, str)):
            return False
        if isinstance(column, str):
            if not (len(column) == 1 and column != ' '):
                return False
            return column in self._letters
        if not (0 < column < 9):
            return False 
        return True
    
    def convert_id(self, value):
        if isinstance(value, UUID):
            return value
        if not isinstance(value, str):
            return
        try:
            return UUID(value)
        except ValueError:
            return
    
    def convert_column(self, column):
        if not self.is_valid_column(column_number):
            return None
        if isinstance(column, str):
            return self._letters.find(column)
        return self._letters[column]

    def cellname_to_pos(self, cellname):
        if not self.is_valid_cellname(cellname):
            return None
        column = self.convert_column(cellname[0])
        row = int(cellname[1])

        real_column = column - 1
        real_row = 8 - row

        return real_row, real_column

    def pos_to_cellname(self, pos):
        if not self.is_valid_pos(pos):
            return None        
        real_row, real_column = pos

        row = 8 - real_row
        column = real_column + 1
        column = self.convert_column(column)

        return f"{column}{row}"

    def get_cell_color(self, cellname):
        pos = self.cellname_to_pos(cellname)
        if not pos:
            return None
        return sum(pos) % 2
