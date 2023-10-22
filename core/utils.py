class Colors:

    WHITE = 'White'
    BLACK = 'Black'


ColorsDict = {
    0: Colors.WHITE,
    1: Colors.BLACK,
}


class Validator:

    _letters = ' ABCDEFGH'

    @classmethod
    def is_valid_cellname(cls, cellname):
        if not isinstance(cellname, str):
            return False
        if len(cellname) != 2:
            return False
        if not cls.is_valid_column(cellname[0]):
            return False
        if not cls.is_valid_row(cellname[1]):
            return False
        return True

    @classmethod
    def is_valid_pos(cls, pos):
        if not isinstance(pos, (tuple, list)):
            return False
        if len(pos) != 2:
            return False
        if not (0 <= pos[0] <= 7):
            return False
        if not (0 <= pos[1] <= 7):
            return False
        return True

    @classmethod
    def is_valid_row(cls, row):
        if not isinstance(row, (int, str)):
            return False
        if isinstance(row, str):
            if not (len(row) == 1 and row.isdigit()):
                return False
            row = int(row)
        if not (0 < row < 9):
            return False
        return True

    @classmethod
    def is_valid_column(cls, column):
        if not isinstance(column, (int, str)):
            return False
        if isinstance(column, str):
            if not (len(column) == 1 and column != ' '):
                return False
            return column in cls._letters
        if not (0 < column < 9):
            return False 
        return True
    
    @classmethod
    def convert_id(cls, value):
        if isinstance(value, UUID):
            return value
        if not isinstance(value, str):
            return
        try:
            return UUID(value)
        except ValueError:
            return
    
    @classmethod
    def convert_column(cls, column):
        if not cls.is_valid_column(column_number):
            return None
        if isinstance(column, str):
            return cls._letters.find(column)
        return cls._letters[column]

    @classmethod
    def cellname_to_pos(cls, cellname):
        if not cls.is_valid_cellname(cellname):
            return None
        column = cls.convert_column(cellname[0])
        row = int(cellname[1])

        real_column = column - 1
        real_row = 8 - row

        return real_row, real_column

    @classmethod
    def pos_to_cellname(cls, pos):
        if not cls.is_valid_pos(pos):
            return None        
        real_row, real_column = pos

        row = 8 - real_row
        column = real_column + 1
        column = cls.convert_column(column)

        return f"{column}{row}"

    @classmethod
    def get_cell_color(cls, cellname):
        pos = cls.cellname_to_pos(cellname)
        if not pos:
            return None
        return sum(pos) % 2
