# chess
Chess game on python, that allows you to create multipe boards and simultaneously have different board with ongoing games.

Here is only implemented the CLI part, but in its core it has an ability to being easily represented via other interfaces, like API servers.

The core controller uses `UUID`s to distinguish boards, but thinking about replacing `UUID`s with random funny names.

P.S. still need to implement timer, [Castling](https://en.wikipedia.org/wiki/Castling) and [en passant](https://en.wikipedia.org/wiki/En_passant)

#### HOW

- To play
> Answer: Run the below command:

`python run.py`

![image](https://github.com/razmikarm/chess/assets/54362304/d39bb7a6-7f30-4457-b90e-606795742d57)

- To make a move
> Answer: Enter the square of the piece and the target sqaure, separated by space. Example`

`D2 D4`

![image](https://github.com/razmikarm/chess/assets/54362304/4d4ec047-4427-43b5-8538-fda572a6761a)

- Get all possible commands
> Answer: type help and press Enter

`help`

![image](https://github.com/razmikarm/chess/assets/54362304/7b7c09de-983f-4619-acdb-adf9f05c4073)

- Know if game is over
> Answer: It automatically recognizes the mate and informs about it

`Here we have a winning situation and when we make the move entered in this screenshot...`

![image](https://github.com/razmikarm/chess/assets/54362304/641dfa13-63d8-4f35-8670-a468281f0e9d)

`The game will end immediatelly`

![image](https://github.com/razmikarm/chess/assets/54362304/4025cabd-b926-41fd-935f-a4f4145b2e19)

