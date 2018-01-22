from utils import *

def search(values):
	"Using depth-first search and propagation, try all possible values."
	# First, reduce the puzzle using the previous function
	values = reduce_puzzle(values)
	if values is False:
		return False ## Failed earlier
	if all(len(values[s]) == 1 for s in boxes): 
		return values ## Solved!
	# Choose one of the unfilled squares with the fewest possibilities
	n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
	# Now use recurrence to solve each one of the resulting sudokus, and 
	for value in values[s]:
		new_sudoku = values.copy()
		new_sudoku[s] = value
		attempt = search(new_sudoku)
		if attempt:
			return attempt