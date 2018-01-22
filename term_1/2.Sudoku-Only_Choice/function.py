from utils import *

rows = 'ABCDEFGHI'
cols = '123456789'
boxes        =  cross(rows, cols)
row_units    = [cross(r, cols) for r  in rows]
column_units = [cross(rows, c) for c  in cols]
square_units = [cross(rs, cs)  for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist     = row_units + column_units + square_units
grid         = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values(grid, starting = True):
		"""
			Convert grid string into {<box>: <value>} dict with '.' value for empties.

			Args:
				grid: Sudoku grid in string form, 81 characters long
			Returns:
				Sudoku grid in dictionary form:
				- keys: Box labels, e.g. 'A1'
				- values: Value in corresponding box, e.g. '8', or '.' if it is empty.
		"""

		gv = {}

		assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
		global boxes
		values = dict(zip(boxes, grid))

		for i in range(len(boxes)):
			if starting:
				if values[boxes[i]] == ".":
					gv[boxes[i]] = "123456789"
				else:
					gv[boxes[i]] = values[boxes[i]]

		return gv


def eliminate(values):
	"""
		Eliminate values from peers of each box with a single value.

		Go through all the boxes, and whenever there is a box with a single value,
		eliminate this value from the set of values of all its peers.

		Args:
			values: Sudoku in dictionary form.
		Returns:
			Resulting Sudoku in dictionary form after eliminating values.
	"""

	values = grid_values(values)

	for box in values.keys():
		peers_lst = list(peers[box])
		if len(values[box]) > 1:
			peers_vals = list(set([values[peer] for peer in peers_lst]))

			eliminated = ""
			for i in "123456789":
				if i not in peers_vals:
					eliminated += i
			values[box] = eliminated
	return values



def only_choice(values):
	"""
		Finalize all values that are the only choice for a unit.

		Go through all the units, and whenever there is a unit with a value
		that only fits in one box, assign the value to this box.

		Input: Sudoku in dictionary form.
		Output: Resulting Sudoku in dictionary form after filling in only choices.
	"""
	# TODO: Implement only choice strategy here

	values = eliminate(values)

	for unit in unitlist:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				values[dplaces[0]] = digit

	return values






display(only_choice(grid))
print("\n\n\n")
display(eliminate(grid))




