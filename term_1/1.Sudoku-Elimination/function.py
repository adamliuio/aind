from utils import *

rows = 'ABCDEFGHI'
cols = '123456789'
boxes        =  cross(rows, cols)
row_units    = [cross(r, cols) for r  in rows]
column_units = [cross(rows, c) for c  in cols]
square_units = [cross(rs, cs)  for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
allvals = "".join("123456789")

def grid_values(grid, starting=True):
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
	boxes =  cross(rows, cols)
	values = [x for x in grid]

	if len(boxes) == len(values):
		for i in range(len(boxes)):
			if starting:
				if values[i] == ".":
					gv[boxes[i]] = "123456789"
				else:
					gv[boxes[i]] = values[i]
		return gv
	else:
		print("oh shit")
		print(len(boxes), len(values))


'''
['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']
['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']
['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']
['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']
['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']
['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']
['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']
['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']
'''


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

	for box in values.keys():
		peers_lst = list(peers[box])
		if len(values[box]) > 1:
			peers_vals = list(set([x for x in "".join(list(set([values[peer] for peer in peers_lst])))]))
			# peers_vals = "".join(peers_vals)
			box_values = [x for x in values[box]]

			for i in box_values:
				if i not in peers_vals:
					if box == "B3": print(i)
					values[box] = i
					break

	return values

display(only_choice(grid_values(grid)))
print("\n\n\n")
display(eliminate(grid_values(grid)))




