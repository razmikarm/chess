class Board:


    def __init__(self):

        self.__matrix = [[None] * 8 for i in range(8)]

    @property
    def state(self):
        return self.__matrix
