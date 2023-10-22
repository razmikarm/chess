

class PromptCLI:

    HINT = (
        "\n"
        "INSTRUCTION:\n"
        "\n"
        "To see all boards enter 'boards'\n"
        "To start new board enter 'new-board'\n"
        "To see current board id enter 'current'\n"
        "To see current board state enter 'show'\n"
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
            'show' : lambda: self._ctrl.show_board(self._curr_board_id),
            'current': lambda: self._curr_board_id,
            'help': lambda: self.HINT,
            'boards': self._ctrl.all_boards,
            'new-board': self._ctrl.start_new_board,
        }

    def set_current_board(self, board_id):
        self._curr_board_id = board_id

    def _get_command(self):
        print("\nTo see all commands enter 'help'")
        command = input('Please, enter your command: ')
        parts = command.strip().split()
        if not parts:
            return
        main = parts[0]
        if (func := self._show_commands.get(main)):
            return print(func())
        if len(parts) != 2:
            print('Invalid command!')
            return
        if (func := self._base_commands.get(main)):
            board_id = parts[1]
            return func(board_id)
        cur_state = self._ctrl.make_move(self._curr_board_id, *parts)
        if not cur_state:
            print(f'Invalid move "{parts}"')


    def show_help(self):
        print(self.HINT)

    def start(self):
        while True:
            self._get_command()
