from.utils import Colors, ColorsDict
from .figure import WHITES_ORDER, BLACKS_ORDER, PAWNS

class Board:

    def __init__(self, id):

        self.__id = id
        self.__matrix = [[None] * 8 for i in range(8)]
        self._turn = 0

        self.set_up()

    @property
    def turn(self):
        return ColorsDict[self._turn]

    def set_up(self):
        self.__matrix[0] = [cls(Colors.BLACK) for cls in BLACKS_ORDER]
        self.__matrix[7] = [cls(Colors.WHITE) for cls in WHITES_ORDER]
        self.__matrix[1] = [cls(Colors.BLACK) for cls in PAWNS]
        self.__matrix[6] = [cls(Colors.WHITE) for cls in PAWNS]

    def make_move(self, from_pos, to_pos):
        from_row, from_column = from_pos 
        to_row, to_column = to_pos 
        figure = self.__matrix[from_row][from_column]
        if self.turn != figure.color:
            return
        if figure.check_move(from_pos, to_pos, self.state):
            self.__matrix[from_row][from_column] = None
            self.__matrix[to_row][to_column] = figure
            self._turn = not self._turn

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return [row.copy() for row in self.__matrix]
