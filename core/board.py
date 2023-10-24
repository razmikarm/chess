from.utils import Colors
from .figure import ORDER, PAWNS

class Board:

    def __init__(self, id):
        self.__id = id
        self.__matrix = [[None] * 8 for i in range(8)]
        self._turn = 0
        self.__history = []

        self.set_up()
        self.__loser = None

    def set_up(self):
        self.__matrix[0] = [cls(Colors.BLACK) for cls in ORDER]
        self.__matrix[1] = [cls(Colors.BLACK) for cls in PAWNS]
        self.__matrix[6] = [cls(Colors.WHITE) for cls in PAWNS]
        self.__matrix[7] = [cls(Colors.WHITE) for cls in ORDER]

    def make_move(self, from_pos, target_pos):
        from_row, from_column = from_pos 
        target_row, target_column = target_pos

        figure = self.__matrix[from_row][from_column]
        if figure is None:
            return {'msg': 'You have entered an empty cell'}
        if self._turn != figure.color:
            return {'msg': 'Not your turn!'}
        target_cell = self.__matrix[target_row][target_column]
        if target_cell and target_cell.color == figure.color:
            return {'msg': "Can't move to busy cell"}

        if figure.can_move(from_pos, target_pos, self.state):
            self.__matrix[target_row][target_column] = figure
            self.__matrix[from_row][from_column] = None
            self._turn = not self._turn
            self.__history.append((from_pos, target_pos))
            self.__loser = figure.check_for_mate(self._turn, self.state)
            return {'msg': 'Move done!'}

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
