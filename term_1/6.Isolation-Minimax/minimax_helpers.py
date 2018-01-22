

"""
	Return True if the game is over for the active player
	and False otherwise.
"""
def terminal_test(gameState):
	if gameState.get_legal_moves() == []:
		return True



"""
	Return the value for a loss (-1) if the game is over,
	otherwise return the maximum value over all legal child nodes.
"""
def max_value(gameState):
	if terminal_test(gameState):
		return -1

	v = float("-inf")
	for a in gameState.get_legal_moves():
		v = max(v, min_value(gameState.forecast_move(a)))
	return v



"""
	Return the value for a win (+1) if the game is over,
	otherwise return the minimum value over all legal child nodes.
"""
def min_value(gameState):
	if terminal_test(gameState):
		return 1

	v = float("inf")
	for a in gameState.get_legal_moves():
		v = min(v, max_value(gameState.forecast_move(a)))
	return v
