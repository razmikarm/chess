from uuid import uuid4, UUID

from .board import Board
from .utils import Validator

class Controller:

    def __init__(self):
        self.boards = {}
        self.archived = {}

    def make_move(self, board_id, from_cell, target_cell):
        board_id = self.convert_id(board_id)
        if not board_id:
            return {'msg': 'Invalid board id'}
        
        if not (board := self.boards.get(board_id)):
            return {'msg': self.game_stat(board_id)}
        
        if (not Validator.is_valid_cellname(from_cell.upper()) or
            not Validator.is_valid_cellname(target_cell.upper())):
            return {'msg': 'The square notation is invalid'}
        
        from_pos = Validator.cellname_to_pos(from_cell.upper())
        target_pos = Validator.cellname_to_pos(target_cell.upper())
        if from_pos == target_pos:
            return {'msg': "Can't make move to the same square"}
        msg = board.make_move(from_pos, target_pos)
        if board.is_over:
            self.game_over(board)
            return {'msg': self.game_stat(board_id)}
        return msg

    def game_stat(self, board_id):
        return self.archived.get(board_id, 'Incorrect board id')

    def game_over(self, board):
        self.archived[board.id] = {
            'winner': board.winner,
            'history': board.history,
        }
        return self.end_board(board.id)

    def start_new_board(self):
        new_id = uuid4()
        self.boards[new_id] = Board(new_id)
        return new_id

    def end_board(self, board_id):
        board_id = self.convert_id(board_id)
        if not board_id:
            return {'msg': 'Invalid board id'}
        if not self.boards.get(board_id):
            return {'msg': 'Incorrect board id'}
        return {'msg': self.boards.pop(board_id)}

    def all_boards(self):
        return list(self.boards.keys())

    def show_board(self, board_id):
        board_id = self.convert_id(board_id)
        if not board_id:
            return {'msg': 'Invalid board id'}
        if not self.boards.get(board_id):
            return {'msg': 'Incorrect board id'}
        return {'msg': self.boards[board_id].state}

    @staticmethod
    def convert_id(value):
        if isinstance(value, UUID):
            return value
        if not isinstance(value, str):
            return
        try:
            return UUID(value)
        except:
            return
