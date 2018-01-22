
from collections import Counter

'''
	The utilities (from previous course materials)
'''

rows = 'ABCDEFGHI'
cols = '123456789'

assignments = []

cross = lambda a, b: [s+t for s in a for t in b]
boxes = cross(rows, cols)

row_units    = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
'''
	Include the 2 diagonal units in the `unitlist` so the program will go through the
	diagonal units as well.
'''
diagonal_units = [[''.join(i) for i in zip(rows, cols)], [''.join(i) for i in zip(rows, cols[::-1])]]
unitlist       = row_units + column_units + diagonal_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)





def checkPuzzle(values):
	'''
	This function is for checking the sudoku solving process
		When there's a single value exist in more than 1 box in each unit in the solution,
		'The Sudoku is wrong.' error is raised
	'''
	for unit in unitlist:
		for box in unit:
			solved_values = [values[box] for box in unit if len(values[box])==1]
			if len(set(solved_values)) != len(solved_values):
				raise ValueError('The Sudoku is wrong.')


''' Original course code '''
def assign_value(values, box, value):
	"""
		Please use this function to update your values dictionary!
		Assigns a value to a given box. If it updates the board record it.
	"""

	# Don't waste memory appending actions that don't actually change any values
	values[box] = value
	if len(value) == 1:
		assignments.append(values.copy())
	return values




def naked_twins(values):
	"""
		Eliminate values using the naked twins strategy.
		Args:
			values(dict): a dictionary of the form {'box_name': '123456789', ...}
		Returns:
			the values dictionary with the naked twins eliminated from peers.
	"""
	'''
		The `cnt.items()` goes through all the units exist in the puzzle,
		`twins` captures the naked twins boxes
		If there are naked twins exist in a unit, eliminate the digits of
		the twins in the twins' peers.
	'''
	for unit in unitlist:
		cnt = Counter(values[box] for box in unit)
		twins = [k for k, c in cnt.items() if len(k) == 2 and c == 2]
		if len(twins) > 0:
			for twin in twins:
				for box in unit:
					if values[box] != twin:
						for digit in twin:
							assign_value(values, box, values[box].replace(digit, ''))
	return values



''' Original course code '''
def grid_values(grid):
	chars, digits = [], '123456789'
	for c in grid:
		if c in digits: chars.append(c)
		if c == '.': chars.append(digits)
	assert len(chars) == 81
	return dict(zip(boxes, chars))



''' Original course code '''
def display(values):
	width = 1+max(len(values[s]) for s in boxes)
	line = '+'.join(['-'*(width * 3)] * 3)
	for r in rows:
		print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
		if r in 'CF': print(line)
	return



''' Original course code '''
def eliminate(values):
	solved = [box for box in values.keys() if len(values[box]) == 1]
	for box in solved:
		digit = values[box]
		for peer in peers[box]:
			assign_value(values, peer, values[peer].replace(digit, ''))
	return values



''' Original course code '''
def only_choice(values):
	values = eliminate(values)
	for unit in unitlist:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				assign_value(values, dplaces[0], digit)
	return values



''' Original course code (modified) '''
def reduce_puzzle(values, naked=True):
	stalled = False
	while not stalled:
		before = len([box for box in values.keys() if len(values[box]) == 1])
		values = only_choice(values)
		if naked:
			values = naked_twins(values)
		after  = len([box for box in values.keys() if len(values[box]) == 1])
		stalled = before == after
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False

	return values



def solve(grid, naked=True):
	'''
		Calls the `search` function (choose to involve the `naked_twins` function or not).
	'''
	return search(grid, naked)




def search(grid, naked=True):
	'''
		Uses the previously defined `eliminate`, `only_choice`, `reduce_puzzle` & `naked_twins`
		functions to reduce the puzzle, and then use recursion to solve the puzzle.
	'''
	values = grid if (type(grid)==dict) else grid_values(grid)
	values = reduce_puzzle(values, naked)

	if values is False:
		return False ## Failed earlier
	if all(len(values[s]) == 1 for s in boxes):
		return values

	_, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
	
	for value in values[s]:
		new_sudoku = values.copy()
		new_sudoku[s] = value
		attempt = solve(new_sudoku)
		if attempt:
			return attempt



if __name__ == '__main__':
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'  # evil
	# display(solve(grid_values(diag_sudoku_grid)))
	display(solve(grid_values(diag_sudoku_grid)))
	checkPuzzle(solve(grid_values(diag_sudoku_grid)))

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



































