class MiniMaxSearchTimeout(Exception):
	def __init__(self, best_move):
		self.best_move = best_move



class SearchTimeout(Exception):
	pass



"""
	Calculate the heuristic value of a game state from the point of view
	of the given player.

	This should be the best heuristic function for your project submission.

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
def custom_score(game, player):

	if game.is_loser(player): return float("-inf")
	if game.is_winner(player): return float("inf")
	my_moves = len(game.get_legal_moves())
	opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

	return float(my_moves**2 / (1 + opponent_moves)) + float(my_moves / (1 + opponent_moves**2))



"""
	Calculate the heuristic value of a game state from the point of view
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
def custom_score_2(game, player):

	if game.is_loser(player): return float("-inf")
	if game.is_winner(player): return float("inf")
	my_moves = len(game.get_legal_moves())
	opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

	return float(my_moves**2 / (1 + opponent_moves))



"""
	Calculate the heuristic value of a game state from the point of view
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
def custom_score_3(game, player):

	if game.is_loser(player): return float("-inf")
	if game.is_winner(player): return float("inf")
	my_moves       = len(game.get_legal_moves())
	opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

	return float(my_moves / (1 + opponent_moves**2))



class IsolationPlayer:
	
	def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
		self.score = score_fn
		self.time_left = None
		self.TIMER_THRESHOLD = timeout
		self.search_depth = search_depth



"""
	Game-playing agent that chooses a move using depth-limited minimax
	search. You must finish and test this player to make sure it properly uses
	minimax to return a good move before the search time limit expires.
"""
class MinimaxPlayer(IsolationPlayer):

	"""
		Search for the best move from the available legal moves and return a
		result before the time limit expires.
		**************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
		For fixed-depth search, this function simply wraps the call to the
		minimax method, but this method provides a common interface for all
		Isolation agents, and you will replace it in the AlphaBetaPlayer with
		iterative deepening search.
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
	def get_move(self, game, time_left):
		self.time_left = time_left

		# Initialize the best move so that this function returns something
		# in case the search fails due to timeout
		best_move = (-1, -1)

		try:
			# The try/except block will automatically catch the exception
			# raised when the timer is about to expire.
			return self.minimax(game, self.search_depth)

		except SearchTimeout:
			pass  # Handle any actions required after timeout as needed

		# Return the best move from the last completed search iteration
		return best_move


	"""
		Implement depth-limited minimax search algorithm as described in
		the lectures.

		This should be a modified version of MINIMAX-DECISION in the AIMA text.
		https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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
				testing.
	"""
	def minimax(self, game, depth):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
		return self.max_value(game, depth)[1]


	"""
		* Modified from previous course material code.
		Return the value for a loss (-1) if the game is over,
		otherwise return the maximum value over all legal child nodes.
	"""
	def max_value(self, game, depth):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
		moves = game.get_legal_moves()

		# return the score and the none move if reaches the max depth of no more legal moves
		if depth <= 0 or not moves:
			return self.score(game, self), (-1, -1)

		best_v = float("-inf")
		best_move = moves[0]

		# start searching
		for move in moves:
			v = best_v
			best_v = max(best_v, self.min_value(game.forecast_move(move), depth-1)[0])
			if best_v != v:
				best_move = move

		return best_v, best_move


	"""
		* Modified from previous course material code.
		Return the value for a win (+1) if the game is over,
		otherwise return the minimum value over all legal child nodes.
	"""
	def min_value(self, game, depth):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
		moves = game.get_legal_moves()

		# return the score and the none move if reaches the max depth of no more legal moves
		if depth <= 0 or not moves:
			return self.score(game, self), (-1, -1)

		best_v = float("inf")
		best_move = moves[0]

		# start searching
		for move in moves:
			v = best_v
			best_v = min(best_v, self.max_value(game.forecast_move(move), depth-1)[0])
			if best_v != v:
				best_move = move

		return best_v, best_move



"""
	Game-playing agent that chooses a move using iterative deepening minimax
	search with alpha-beta pruning. You must finish and test this player to
	make sure it returns a good move before the search time limit expires.
"""
class AlphaBetaPlayer(IsolationPlayer):

	"""
		Search for the best move from the available legal moves and return a
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
	def get_move(self, game, time_left):

		self.time_left = time_left
		moves = game.get_legal_moves()
		if not moves: return -1, -1

		move = moves[0]
		depth = 1

		try:
			while True:
				move = self.alphabeta(game, depth)
				depth += 1
		except SearchTimeout:
			return move

		return move


	"""
		Implement depth-limited minimax search with alpha-beta pruning as
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
				testing.
	"""
	def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
		return self.ab_max_value(game, depth)[1]


	"""
		Implemented with alpha beta prunning.
		Return the value for a loss (-1) if the game is over,
		otherwise return the maximum value over all legal child nodes.
	"""
	def ab_max_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

		if depth == 0:
			 return self.score(game, self), (-1, -1)
		if game.utility(self) != 0.0:
			return game.utility(self), (-1, -1)

		moves     = game.get_legal_moves()
		best_move = moves[0]

		for move in moves:

			v, _ = self.ab_min_value(game.forecast_move(move), depth-1, alpha, beta)
			if v > alpha: alpha, best_move = v, move
			if alpha >= beta: break

		return alpha, best_move


	"""
		Implemented with alpha beta prunning.
		Return the value for a win (+1) if the game is over,
		otherwise return the minimum value over all legal child nodes.
	"""
	def ab_min_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):

		if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

		if depth == 0:
			 return self.score(game, self), (-1, -1)
		if game.utility(self) != 0.0:
			return game.utility(self), (-1, -1)

		moves     = game.get_legal_moves()
		best_move = moves[0]

		for move in moves:

			v, _ = self.ab_max_value(game.forecast_move(move), depth-1, alpha, beta)
			if v < beta: beta, best_move = v, move
			if alpha >= beta: break

		return beta, best_move













