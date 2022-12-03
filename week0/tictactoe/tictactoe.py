"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_count = 0
    o_count = 0

    # count all X and O on the board
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    # x starts first
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # looks for empty cells
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    if result_board[action[0]][action[1]] is None:
        result_board[action[0]][action[1]] = player(board)
        return result_board
    else:
        raise Exception("Invalid Move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # row winning
    for row in board:
        if row[0] is not None and all(cell == row[0] for cell in row):
            return row[0]

    # column winning
    for i in range(3):
        if board[0][i] is not None and all(board[0][i] == row[i] for row in board):
            return board[0][i]

    # diagonal winning
    if board[0][0] is not None and all(board[0][0] == board[i][i] for i in range(3)):
        return board[0][0]
    elif board[2][0] is not None and board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:
        for row in board:
            for cell in row:
                if cell is None:
                    return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    elif win == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        return max_value(board)[1]
    elif player(board) == O:
        return min_value(board)[1]


def max_value(board):
    # check if game ended
    if terminal(board):
        return utility(board), None

    else:
        v = -2
        next_move = None

        for action in actions(board):
            new_v = max(v, min_value(result(board, action))[0])
            if new_v > v:
                v = new_v
                next_move = action
                if v == 1:
                    break

        return v, next_move


def min_value(board):
    # check if game ended
    if terminal(board):
        return utility(board), None

    else:
        v = 2
        next_move = None

        for action in actions(board):
            new_v = min(v, max_value(result(board, action))[0])
            if new_v < v:
                v = new_v
                next_move = action
                if v == -1:
                    break

        return v, next_move