# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 11:58:47 2018

@author: 5219294
"""

"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
#import random
#from isolation.isolation import Board
#import random
class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    #modified the get_moves function in isolation.py
    #x is the dictionary of avilable open legal moves for each cell given the board state
    x = dict((a, game.get_valid_moves(a)) for a in game.get_blank_spaces())
    l=0
    #caluculating potential sum of look ahead moves for the student player.
    for m in game.get_legal_moves(player):
    #l will accumulate the sum of all legal moves avilable in the look ahead play instead of just next play
        l=l+len(x[m])
    lo=0
    #caluculating potential sum of look ahead moves for the opponent player.
    for m in game.get_legal_moves(game.get_opponent(player)):
        lo=lo+len(x[m])
    #huerestic will return the differnce of sum of look ahead moves for student
    return float(l-lo)



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    x = dict((a, game.get_valid_moves(a)) for a in game.get_blank_spaces())
    l=0
    for m in game.get_legal_moves(player):
        #print(m,len(x[m]))
        l=l+len(x[m])
    return float(l)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    x = dict((a, game.get_valid_moves(a)) for a in game.get_blank_spaces())
    l=0
    for m in  game.get_legal_moves(game.get_opponent(player)):
        #print(m,len(x[m]))
        l=l+len(x[m])
    return float(- l)


class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        self.best_move = (-1, -1) 
        #exception handaling
        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            return self.best_move


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        #time check
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if not game.get_legal_moves():
            return (-1, -1)  
        alpha = float("-inf")
        for m in game.get_legal_moves():
            updated_game = game.forecast_move(m)
            score_best = self.min_player(updated_game,depth-1)
            if score_best > alpha:
                alpha = score_best
                self.best_move = m
        return self.best_move

    def max_player(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game,game.active_player)
        alpha = float("-inf")
        for m in game.get_legal_moves():
            updated_game = game.forecast_move(m)
            score_min = self.min_player(updated_game,depth-1)
            alpha=max(score_min,alpha)
        return alpha        

    def min_player(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game,game.inactive_player)
        beta = float("inf")
        for m in game.get_legal_moves():
            updated_game = game.forecast_move(m)
            score_max = self.max_player(updated_game,depth-1)
            beta=min(score_max,beta)
        return beta 
	
	

class AlphaBetaPlayer(IsolationPlayer):

    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        #implementing iterative deepening.
        self.time_left = time_left
        self.best_move= (-1,-1)
        for i in range(1,10000):
            try:
                best_move=self.alphabeta(game,i)
            except SearchTimeout:
                #break
                return best_move
                


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing."""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if not game.get_legal_moves():
            return(-1, -1)
        return(self.alpha_max_player(game,depth,alpha,beta)[1])
            
       
    def alpha_max_player(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            
            return (self.score(game,game.active_player),game.get_player_location(game.active_player))
        
        #print('legal moves in Max_play'.format(moves))
        best_score_max = float("-inf")
        best_move=None
        for m in game.get_legal_moves():
            #self.checktimer()
            
            updated_game = game.forecast_move(m)
            score_min = self.alpha_min_player(updated_game,depth-1,alpha,beta)[0]
            
            if score_min >  best_score_max:
               
                best_score_max = score_min
                
                best_move=m
                
            if best_score_max >= beta:
                
                return best_score_max,best_move
           
            alpha=max(alpha,best_score_max)
        return alpha,best_move,game.active_player      

    def alpha_min_player(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:

            return (self.score(game,game.inactive_player),game.get_player_location(game.inactive_player))
        best_score_min = float("inf")
        best_move=None
        for m in game.get_legal_moves():
            
            updated_game = game.forecast_move(m)
            score_max = self.alpha_max_player(updated_game,depth-1,alpha,beta)[0]
           
            if score_max < best_score_min:
                best_score_min = score_max
                best_move=m
    
            if best_score_min <= alpha:
                   
                    return best_score_min,best_move
            
            beta=min(beta,best_score_min)

        return beta,best_move,game.active_player      

