"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0
    for row in board:
        for col in row:
            if col == X:
                num_x += 1
            elif col == O:
                num_o += 1
    if num_x > num_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    _actions = set()
    row_pos = 0
    for row in board:
        col_pos = 0

        for col in row:
            if col == None:
                _actions.add((row_pos, col_pos))
            col_pos += 1
        row_pos += 1

    return _actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy
    new_board = copy.deepcopy(board)
    _i, _j = action

    if new_board[_i][_j] != None:
        raise Exception("Invalid Action")

    if player(board) == X:
        new_board[_i][_j] = X
    elif player(board) == O:
        new_board[_i][_j] = O

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def check_win(_x):
        for i in range(3):
            if board[i] == [_x,_x,_x] or [x[i] for x in board] == [_x,_x,_x]:
                return True

        if (board[0][0] ==_x and board[1][1] == _x and board[2][2] == _x) or (board[0][2] ==_x and board[1][1] == _x and board[2][0] == _x):
            return True

    if check_win(O):
        return O
    elif check_win(X):
        return X
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for row in board:
            if None in row:
                return False
        return True

    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    elif winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board):
        if terminal(board):
            return utility(board), tuple()

        v = -99999

        for action in actions(board):
            _min_value = min_value(result(board,action))[0]
            if _min_value > v:

                v = _min_value
                _action = action

        return v, _action

    def min_value(board):
        if terminal(board):
            return utility(board), tuple()

        v = 99999

        for action in actions(board):
            _max_value = max_value(result(board,action))[0]
            if _max_value < v:
                
                v = _max_value
                _action = action

        return v, _action


    if player(board) == O:
        return min_value(board)[1]
        
    elif player(board) == X:
        return max_value(board)[1]
