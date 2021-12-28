import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None




def initial_state():
    """
    Returns starting state of the board.
    """
    return [[None, None, O],
            [None, X, None],
            [None, X, None]]

a=initial_state()

# print(ttt.player(initial_state()))

print(ttt.minimax_(initial_state()))

# print(ttt.max_value(initial_state()))

# print(ttt.winner(ttt.result(initial_state(),))