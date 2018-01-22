
# alpha-beta-pruning algorithm, AIMA P.190

def alpha_beta_search(gameState):
	v = max_value(gameState, float("-inf"), float("inf"))
	


## from game state

"""
	Returns True if the game is over for the active player
	and False otherwise.
"""
def terminal_test(gameState, alpha=float("-inf"), beta=float("inf")):
	return gameState.get_legal_moves() == []



"""
	Return the value for a loss (-1) if the game is over,
	otherwise return the maximum value over all legal child
	nodes.
"""
def max_value(gameState, alpha=float("-inf"), beta=float("inf")):

	if terminal_test(gameState):
		return -1
	v = float("-inf")

	for ac in gameState.get_legal_moves():
		v = max(v, min_value(gameState.forecast_move(ac), alpha, beta))
		if v >= beta:
			return v
		alpha = max(alpha, v)
	return v



"""
	Return the value for a win (+1) if the game is over,
	otherwise return the minimum value over all legal child
	nodes.
"""
def min_value(gameState, alpha=float("-inf"), beta=float("inf")):

	if terminal_test(gameState):
		return 1
	v = float("inf")

	for ac in gameState.get_legal_moves():
		v = min(v, max_value(gameState.forecast_move(ac), alpha, beta))
		if v <= alpha:
			return v
		beta = min(beta, v)
	return v



