"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

from numpy import empty

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
    set_of_actions = set()
    if terminal(board):
        set_of_actions.add((0, 0))    
    else:        
        for row in range(3):
            for elem in range(3):
                if board[row][elem] == EMPTY:
                    set_of_actions.add((row, elem))                  
    return set_of_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        return board

    if not (0 <= action[0] < 3) or not (0 <= action[1] < 3):
        raise Exception("Invalid action")
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action")
    board1 = deepcopy(board)
    if player(board1) == X:
        board1[action[0]][action[1]] = X        
    else:    
        board1[action[0]][action[1]] = O        
        
    return board1    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    """if board == [[EMPTY, EMPTY, X],
            [EMPTY, O, X],
            [EMPTY, O, X]]:
            print(board)"""
    if countboard(board) <= 4:        
        return None
    else:
        # Go through rows
        for row in board:
            if row[0] == row[1] and row[1] == row[2] and row[0] != EMPTY :
                return row[0]
        # Go through columns:        
        for col in range(3):
            i=0
            aux = board[i][col]
            ok = True
            while board[i][col] == aux and ok and aux != EMPTY:
                if (i+1 < 3):
                    i += 1
                else:                    
                    ok = False
            if not ok:
                return aux
        # Go through diagonals
        if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
            return board[0][0]  

        if (board[0][2] == board[1][1] and board[1][1] == board[2][0]) and board[0][2] != EMPTY:
            return board[0][2]

        # tied game
        return None                


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    w = winner(board)  
    #print(board) 
    #print(w) 
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
    if terminal(board):    
        return None
    else:
        if player(board) == X:
            return maxaction(board, None)[0]
        else:    
            return minaction(board, None)[0]    


def minaction(board, aux):        
    # invoked by player O
    
    pos_actions = actions(board)
    
    minutility = 1
    minaction_var = None

    for action in pos_actions:
        if minaction_var == None:
            minaction_var = action
    
    for action in pos_actions:        
        nboard = result(board, action)
        # O chooses the min of the next max moves
        # X
        if terminal(nboard):    

            if utility(nboard) < minutility:
                minutility =  utility(nboard)
                minaction_var = action 

            if aux != None:
                if utility(nboard) <= aux:  
                    break                 

        # O chooses the min of the next max moves
        # X chooses the max of the next min moves
        # O    
        else:
            max_utility = maxaction(nboard)[1]
            if aux == None:
                aux = max_utility
            if max_utility < minutility:
                minutility =  max_utility
                minaction_var = action                           
    
    return minaction_var, minutility        


def maxaction(board, aux):        
    # invoked by player X
    
    pos_actions = actions(board)
    maxutility = -1
    maxaction_var = None
   

    for action in pos_actions:
        if maxaction_var == None:
            maxaction_var = action

    for action in pos_actions:        
        nboard = result(board, action)
        # X chooses the max of the next min moves
        # O
        if terminal(nboard): 
            if utility(nboard) > maxutility:
                maxutility =  utility(nboard)
                maxaction_var = action

        # X chooses the max of the next min moves
        # O chooses the min of the next max moves
        # X    
        else:
            min_utility = minaction(nboard, aux)[1]
            if aux == None:
                aux = min_utility
            elif min_utility > aux:
                aux = min_utility    
            if  min_utility > maxutility:
                maxutility =  min_utility
                maxaction_var = action        

    return maxaction_var, maxutility    


def countboard(board):
    count = 0
    for row in board:
        for elem in range(3):   
            if row[elem] != EMPTY:
                count += 1                
    return count