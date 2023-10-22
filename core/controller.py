from uuid import uuid4, UUID

from .board import Board
from .utils import Colors, Validator

class Controller:

    def __init__(self):
        self.boards = {}

    def make_move(self, board_id, from_cell, to_cell):
        board_id = self.convert_id(board_id)
        if not board_id:
            return
        if not (board := self.boards.get(board_id)):
            return
        if not Validator.is_valid_cellname(from_cell):
            return
        if not Validator.is_valid_cellname(to_cell):
            return
        from_pos = Validator.cellname_to_pos(from_cell)
        to_pos = Validator.cellname_to_pos(to_cell)
        state = board.make_move(from_pos, to_pos)
        if board.loser:
            self.game_over(board)

    def game_over(self, board):
        pass # TODO: Implement actions when the game is over | loser can be accessed by board.loser

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
