import os

from .figure import TEXT_FIGURES
from .utils import COLOR_NAMES, Validator

class PromptCLI:

    HINT = (
        "\n"
        "INSTRUCTION:\n"
        "\n"
        "To see all boards enter 'boards'\n"
        "To start new board enter 'new-board'\n"
        "To see current board id enter 'current'\n"
        "To remove the board enter 'remove-board <board id>'\n"
        "To choose the board enter 'set-board <board id>'\n"
        "\n"
        "To make move enter '<FROM> <TO>', where\n"
        "<FROM> and <TO> should be represented as square notations\n\n"
        "Examples:\n"
        "'A2 E2'\n"
        "'F8 C3'\n"
        "'H4 H7'"
    )


    def __init__(self, controller):
        self._ctrl = controller
        self._curr_board_id = self._ctrl.start_new_board()


        self._base_commands = {
            'set-board': self.set_current_board,
            'remove-board': self._ctrl.end_board,
        }
        self._unar_commands = {
            'help': self.show_help,
            'current': self.get_current_board,
            'boards': self.show_all_boards,
            'new-board': self.create_new_board,
        }

    def create_new_board(self):
        self._curr_board_id = self._ctrl.start_new_board()

    def show_all_boards(self):
        return ' | '.join(str(id) for id in self._ctrl.all_boards())

    def set_current_board(self, board_id):
        self._curr_board_id = board_id

    def get_current_board(self):
        return self._curr_board_id

    def __command_parser(self, parts):
        if not parts:
            return (lambda: 'Invalid command!'),
        main = parts[0]
        if (func := self._unar_commands.get(main)):
            return func,
        if len(parts) != 2:
            return (lambda: 'Invalid command!'),
        if (func := self._base_commands.get(main)):
            board_id = parts[1]
            return func, board_id

    def _get_command(self):
        print("To see all commands enter 'help'")
        command = input('Enter your move/command: ').lower()
        self.clear()

        parts = command.strip().split()
        parsed = self.__command_parser(parts)
        if parsed is None:
            result = self._ctrl.make_move(self._curr_board_id, *parts)
        else:
            func, *args = parsed
            parsed_msg = func(*args)
        self.show_board()
        if parsed is not None:
            if parsed_msg is not None:
                print(parsed_msg)
            return
        
        message = result['msg']
        if isinstance(message, str):
            print(message)
        elif isinstance(message, dict):
            print(f"{COLOR_NAMES[message['winner']]} player won")
            print("Game history:")
            for i, move in enumerate(message['history'], start=1):
                from_pos, target_pos = move
                from_cell = Validator.pos_to_cellname(from_pos)
                target_cell = Validator.pos_to_cellname(target_pos)
                print(f"{i:02}| {from_cell} -> {target_cell}")

    def show_board(self, board=None):
        if board is None:
            result = self._ctrl.show_board(self._curr_board_id)
            if isinstance(result['msg'], str):
                print(result['msg'])
                print('\nStart new board')
                return
            board = result['msg']
        mid_line = '-' * 34
        view = f'\n{mid_line}\n'
        for i, row in enumerate(board):
            view = f"{view}{8 - i}| "
            for figure in row:
                if figure is None:
                    symbol = ' '
                else:
                    symbol = TEXT_FIGURES[figure.color][figure.__class__]
                view = f"{view}{symbol} | "
            view = f"{view}\n{mid_line}\n"
        view = f"{view}   {' * '.join('ABCDEFGH')}\n"
        print(view)
        return view

    def clear(self):
        if os.name == 'posix':
            os.system("clear")
        else:
            os.system("cls")

    def show_help(self):
        return self.HINT

    def start(self):
        self.show_board()
        while True:
            self._get_command()
