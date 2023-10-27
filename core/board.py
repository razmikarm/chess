from dataclasses import dataclass

from utils import Colors
from figure import ORDER, PAWNS, Figure


@dataclass
class Move:

    prev = None
    figure: Figure
    start: tuple
    target: tuple
    state: list
    next = None


class History:

    def __init__(self):
        self.__first_move = None
        self.__last_move = None
        self.__by_figure = {}

    def register(self, move):
        figure = move.figure
        figure_moves = self.__by_figure.get(figure, [])
        figure_moves.append(move)
        self.__by_figure[figure] = figure_moves

        move.prev = self.__last_move
        self.__last_move.next = move
        self.__last_move = move

    @property
    def last_move(self):
        return self.__last_move

    @property
    def first_move(self):
        return self.__first_move
    
    def get_figure_moves(self, figure):
        return self.__by_figure.get(figure, [])
    
    def moves(self, reverse=False):
        curr = self.first_move
        attr = 'next'
        if reverse:
            curr = self.last_move
            attr = 'prev'
        while curr:
            yield curr
            curr = getattr(curr, attr)


class Board:

    def __init__(self, id):
        self.__id = id
        self.__matrix = [[None] * 8 for i in range(8)]
        self._turn = 0
        self.__history = History()

        self.set_up()
        self.__loser = None

    def set_up(self):
        self.__matrix[0] = [cls(Colors.BLACK) for cls in ORDER]
        self.__matrix[1] = [cls(Colors.BLACK) for cls in PAWNS]
        self.__matrix[6] = [cls(Colors.WHITE) for cls in PAWNS]
        self.__matrix[7] = [cls(Colors.WHITE) for cls in ORDER]

    def make_move(self, start_pos, target_pos):
        start_row, start_column = start_pos 
        target_row, target_column = target_pos

        figure = self.__matrix[start_row][start_column]
        if figure is None:
            return {'msg': 'You have entered an empty cell'}
        if self._turn != figure.color:
            return {'msg': 'Not your turn!'}
        target_cell = self.__matrix[target_row][target_column]
        if target_cell and target_cell.color == figure.color:
            return {'msg': "Can't move to busy cell"}

        move = Move(figure, start_pos, target_pos, self.state)

        if figure.can_move(start_pos, target_pos, self.state):
            self.__matrix[target_row][target_column] = figure
            self.__matrix[start_row][start_column] = None
            self._turn = not self._turn
            self.__history.register(move)
            self.__loser = figure.check_for_mate(self._turn, self.state)
            return {'msg': 'Move done!'}
        return {'msg': 'The move is impossible'}

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return [row.copy() for row in self.__matrix]

    @property
    def history(self):
        return self.__history

    @property
    def winner(self):
        return not self.__loser

    @property
    def is_over(self):
        return self.__loser is not None
