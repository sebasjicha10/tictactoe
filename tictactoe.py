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
    # Keep track of moves
    xMoves = 0
    oMoves = 0

    # Add moves
    for line in board:
        for move in line:
            if move == X:
                xMoves = xMoves + 1
            elif move == O:
                oMoves = oMoves + 1
    
    # Player O goes only when Player X has made more moves
    if xMoves > oMoves:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Possible actions
    actions = set()

    # Iterate board and populate actions 
    for (i, line) in enumerate(board):
        for (j, row) in enumerate(line):
            if row == EMPTY:
                actions.update([(i, j)])

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Validate action
    if action not in actions(board):
        raise Exception("Invalid Move")

    # Deep copy board
    test_board = copy.deepcopy(board)

    # Select Player
    next_player = player(board)

    # Add move
    test_board[action[0]][action[1]] = next_player

    return test_board
  

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Make a list with all the board positions
    board_list = []
    for line in board:
        for move in line:
            board_list.append(move)

    # Returns winner if there is one
    def find_winner(x, y, z):
        if board_list[x] == board_list[y] == board_list[z] and board_list[x] != EMPTY:
            return board_list[x]

    # Look for a winner combination
    return ( 
        find_winner(0, 3, 6) or 
        find_winner(1, 4, 7) or 
        find_winner(2, 5, 8) or 
        find_winner(0, 1, 2) or 
        find_winner(3, 4, 5) or 
        find_winner(6, 7, 8) or 
        find_winner(0, 4, 8) or 
        find_winner(2, 4, 6) 
    )


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) or actions(board) == set():
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1
    else: 
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Validate board
    if terminal(board):
        return None

    # Max algorithm
    def max_value(state):
        if terminal(state):
            return utility(state)
        value = -1
        for action in actions(state):
            value = max(value, min_value(result(state, action)))
        return value

    # Min algorithm 
    def min_value(state):
        if terminal(state):
            return utility(state)
        value = 1
        for action in actions(state):
            value = min(value, max_value(result(state, action)))
        return value

    # Select optimal action
    selected_action = tuple()
    next_player = player(board)


    # Handle AI for MIN player
    if next_player == O:
        value = 1
        for action in actions(board):
            if max_value(result(board, action)) < value:
                value = max_value(result(board, action))
                selected_action = action

    # Handle AI for MAX player
    if next_player == X:

        # Very first move of X
        if board == initial_state():
            selected_action = (0, 0)

        else:
            value = -1
            for action in actions(board):
                if min_value(result(board, action)) > value:
                    value = min_value(result(board, action))
                    selected_action = action

    return selected_action