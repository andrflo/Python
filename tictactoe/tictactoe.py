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
    if board == [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]] or terminal(board):
        return X    
    else:
        count = countboard(board)
        if count % 2 == 0:
            return X
        else:
            return O     

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return set()
    else:
        set_of_actions = set()
        for row in range(3):
            for elem in range(3):
                if board[row][elem] == EMPTY:
                    set_of_actions.add((row, elem))
        return set_of_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if player(board) == X:
        board[action(0)][action(1)] = X
    else:    
        board[action(0)][action(1)] = O
    return board    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if countboard(board) <= 4:
        return None
    else:
        # Go through rows
        for row in board:
            if row[0] == row[1] and row[1] == row[2]:
                return row[0]
        # Go through columns:        
        for col in range(3):
            i=0
            aux = board[i][col]
            while board[i][col] == aux and i < 3:
                i+=1
            if i == 3:
                return aux
        # Go through diagonals
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]  

        if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
            return board[0][2]

        return None                        



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    w = winner(board)
    if w != X and w != O:
        count = countboard(board)
        return True if count == 9 else False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    match winner(board):
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0        


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

def countboard(board):
    count = 0
    for row in board:
        for elem in row:   
            if board[row][elem] != EMPTY:
                count += 1 
    return count