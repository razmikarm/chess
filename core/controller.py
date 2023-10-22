from uuid import uuid4, UUID

from .board import Board
from .utils import Colors, Validator

class Controller:

    def __init__(self):
        self.boards = {}
        self.finished = {}

    def make_move(self, board_id, from_cell, to_cell):
        board_id = self.convert_id(board_id)
        if not board_id:
            return
        if not (board := self.boards.get(board_id)):
                return self.game_stat(board_id)
        if not Validator.is_valid_cellname(from_cell.upper()):
            return
        if not Validator.is_valid_cellname(to_cell.upper()):
            return
        from_pos = Validator.cellname_to_pos(from_cell.upper())
        to_pos = Validator.cellname_to_pos(to_cell.upper())
        if from_pos == to_pos:
            return
        state = board.make_move(from_pos, to_pos)
        if board.loser is not None:
            print("The game is over")
            self.game_over(board)
            return self.game_stat(board_id)
        return state

    def game_stat(self, board_id):
        return self.finished.get(board_id)

    def game_over(self, board):
        self.finished[board.id] = {
            'winner': not board.loser,
            'history': board.history,
        }
        self.end_board(board.id)
        
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

    @staticmethod
    def convert_id(value):
        if isinstance(value, UUID):
            return value
        if not isinstance(value, str):
            return
        try:
            return UUID(value)
        except ValueError:
            return
