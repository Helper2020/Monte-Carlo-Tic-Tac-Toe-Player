"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 5      # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
    This function runs the monte carlo trials
    of the current state of the board
    """
    
    while(board.check_win() == None):
        empty_squares = board.get_empty_squares()
        square = random.choice(empty_squares)
        board.move(square[0], square[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function scores the current state of a
    mc game.
    
    inputs:
    Scores - Is a list of list with the same dimensions of
              a tic-tac-toe board.
    board  - Is a TTTBoard object of a completed game
    player - player is the player that is the machine
    
    outputs:
    This funcion does not return anything
    It modifes the scores grid
    """
    out_come = board.check_win()
    
    if out_come == player:
        score_winning_game(scores, board, player)
    elif out_come == provided.switch_player(player):
        score_losing_game(scores, board, player)
    else:
         score_tie_game(scores, board)
    
   

def score_winning_game(scores, board, player):
    """
    This function scores a winning mc game
    
    inputs:
    Scores - Is a list of list with the same dimensions of
              a tic-tac-toe board.
    board  - Is a TTTBoard object of a completed game
    player - player is the player that is the machine
    
    outputs:
    This funcion does not return anything
    It modifes the scores grid
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) != provided.EMPTY:
                if board.square(row,col) == player:
                    scores[row][col] = scores[row][col] + SCORE_CURRENT
                else:
                    scores[row][col] =  scores[row][col] + -1 * SCORE_OTHER
                
def score_losing_game(scores, board, player):
    """
    This function scores a losing mc game
    
    inputs:
    Scores - Is a list of list with the same dimensions of
              a tic-tac-toe board.
    board  - Is a TTTBoard object of a completed game
    player - player is the player that is the machine
    
    outputs:
    This funcion does not return anything
    It modifes the scores grid
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row,col) != provided.EMPTY:
                if board.square(row,col) == player:
                    scores[row][col] =  scores[row][col] + -1 * SCORE_OTHER
                else:
                    scores[row][col] = scores[row][col] + SCORE_CURRENT

def score_tie_game(scores, board):
    """
    This function scores a tied mc game
    
    inputs:
    Scores - Is a list of list with the same dimensions of
              a tic-tac-toe board.
    board  - Is a TTTBoard object of a completed game
    
    outputs:
    This funcion does not return anything
    It modifes the scores grid
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            scores[row][col] = scores[row][col] + 0

def get_best_move(board, scores):
    """
    This function finds all the empty square of game
    then determines the best movie
    
    inputs:
    Scores - Is a list of list with the same dimensions of
             a tic-tac-toe board.
    board  - Is a TTTBoard object of a completed game
    
    outputs:
    This funcion returns a tuple that represents the move
    """
    
    empty_sq_list = board.get_empty_squares()
    max_score = None
    max_sq_list = []
    if len(empty_sq_list) == 0:
        return ()

    for emp_sq in empty_sq_list:
        if max_score == None:
            max_score = scores[emp_sq[0]][emp_sq[1]]
        elif scores[emp_sq[0]][emp_sq[1]] >= max_score:
            max_score = scores[emp_sq[0]][emp_sq[1]]
           
    for emp_sq in empty_sq_list:
        if scores[emp_sq[0]][emp_sq[1]] == max_score:
            max_sq_list.append(emp_sq)
            
    return random.choice(max_sq_list)

def mc_move(board, player, trials):
    """
    This function determines the best move from
    a number of mc trials
    
    input:
    board  - Is a TTTBoard object 
    player - Is the machine player
    trial  - Number of mc trials to run
    
    output:
    This function returns the best move from a number of trials
    """
    
    total_scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
    for dummy_trial in range(trials):
        curr_board = board.clone()
        mc_trial(curr_board, player)
               
        scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
        mc_update_scores(scores, curr_board, player)
        best_move = get_best_move(board,scores)
        total_scores[best_move[0]][best_move[1]] = total_scores[best_move[0]][best_move[1]] + 1  
     

    return get_best_mc_move(total_scores)

def get_best_mc_move(total_scores):
    """
    This function determine the best move after MC trials
    
    input:
    total_scores - A list of list of scores for each square in on the board
    
    output:
    This function output a tuple that has the row and col
    """
    
    max_score = None
    max_row = 0
    max_col = 0
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if max_score == None:
                max_score = total_scores[max_row][max_col]
            elif total_scores[row][col] > max_score:
                max_row = row
                max_col = col
    
    return (max_row, max_col)
            
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
