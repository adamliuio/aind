from utils import *

# boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......' # original
# grid="2.74...1...9163.7...1.7...674.6........7.1........4.253...4.1...8.9173...9...54.7" # medium
# grid="..15..6...3..24....4.1.7....6.3...9...5.7.4...7...1.3....8.6.1....29..4...9..32.." # hard
# grid="..645....9..2.3....1...82.4..8....5.3.......7.9....6..1.79...4....7.1..9....453.." # eval
grid='2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
grid='4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid = "9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................"

display(grid_values(grid, dot=True))
print()
display(eliminate(grid_values(grid)))

def search(values):
	from itertools import compress
	"Using depth-first search and propagation, create a search tree and solve the sudoku."
	# First, reduce the puzzle using the previous function

	values = reduce_puzzle(values)
	if values is False:
		return False
	if all(len(values[s]) == 1 for s in boxes):
		return values
	
	# Choose one of the unfilled squares with the fewest possibilities
	n, s = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

	# Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

	for try_d in values[s]:
		values_new = values.copy()
		values_new[s] = try_d
		attempt = search(values_new)
		if attempt:
			return attempt

display(search(grid_values(grid)))