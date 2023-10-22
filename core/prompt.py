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
        "<FROM> and <TO> should be represented as cellname\n\n"
        "Examples:\n"
        "'A2 E2'\n"
        "'F8 C3'\n"
        "'H4 H7'\n"
    )


    def __init__(self, controller):
        self._ctrl = controller
        self._curr_board_id = self._ctrl.start_new_board()


        self._base_commands = {
            'set-board': self.set_current_board,
            'remove-board': self._ctrl.end_board,
        }
        self._show_commands = {
            'help': self.show_help,
            'new-board': self._ctrl.start_new_board,
            'current': lambda: print(self._curr_board_id),
            'boards': lambda: print(self._ctrl.all_boards()),
        }

    def set_current_board(self, board_id):
        self._curr_board_id = board_id

    def _get_command(self):
        print("\nTo see all commands enter 'help'")
        command = input('Please, enter your command: ').lower()
        self.clear()
        parts = command.strip().split()
        if not parts:
            return
        main = parts[0]
        if (func := self._show_commands.get(main)):
            return func()
        if len(parts) != 2:
            print('Invalid command!')
            return
        if (func := self._base_commands.get(main)):
            board_id = parts[1]
            return func(board_id)
        cur_state = self._ctrl.make_move(self._curr_board_id, *parts)
        if isinstance(cur_state, dict):
            print('Game is over!')
            print(f"{COLOR_NAMES[cur_state['winner']]} player won")
            print("Game history:")
            for i, move in enumerate(cur_state['history'], start=1):
                from_pos, to_pos = move
                from_cell = Validator.pos_to_cellname(from_pos)
                to_cell = Validator.pos_to_cellname(to_pos)
                print(f"{i:02} ) {from_cell} -> {to_cell}")
        # if not cur_state:
        #     print(f'Invalid move "{parts[0].upper()} -> {parts[1].upper()}"')

    def show_board(self, board=None):
        if board is None:
            board = self._ctrl.show_board(self._curr_board_id)
        if board is None:
            print('Start new board')
            return
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
        view = f"{view}   {' * '.join('ABCDEFGH')}"
        print(view)
        return view

    def clear(self):
        if os.name == 'posix':
            os.system("clear")
        else:
            os.system("cls")

    def show_help(self):
        print(self.HINT)

    def start(self):
        while True:
            self.show_board()
            self._get_command()
