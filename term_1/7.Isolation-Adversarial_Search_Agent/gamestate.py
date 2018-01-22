
from copy import deepcopy

class GameState:

	def __init__(self):

		# define the board size
		self._nrows = 2
		self._ncols = 3
		self.board  = [[None] * self._ncols for _ in range(self._nrows)]
		del self.board[1][2]

		self.board_pos = [(a, b) for a in range(self._nrows) for b in range(self._ncols)][:-1]

		self.taken_moves = []
		self.active_player = 0
		self.player_positions = [None, None]
		self.directions = [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1] if (a,b)!=(0,0)]



	"""
		Return a new board object with the specified move
		applied to the current game state.
		
		Parameters
		----------
		move: tuple
			The target position for the active player's next move
	"""
	def forecast_move(self, move):

		if move not in self.get_legal_moves():
			raise Exception("Illegal move.")

		new_board = deepcopy(self)
		new_board.board[move[0]][move[1]] = new_board.active_player
		new_board.taken_moves.append(move)
		new_board.player_positions[self.active_player] = move
		new_board.active_player ^= 1
		return new_board



	"""
		Return a list of all legal moves available to the active player.
		Each player should get a list of all empty spaces on the board on their first move,
		and otherwise they should get a list of all open spaces in a straight line along any row,
		column or diagonal from their current position. (Players CANNOT move through obstacles or blocked squares.)
		Moves should be a pair of integers in (column, row) order specifying the zero-indexed coordinates on the board.
	"""
	def get_legal_moves(self):

		# if the board is blank, return all the empty spaces
		if self.taken_moves == []:
			available_moves = [(a, b) for a in range(self._nrows) for b in range(self._ncols)][:-1]
			return available_moves

		# if the activate player haven't make a move, return all the empty spaces except the opponent's moves
		if self.player_positions[self.active_player] == None and len(self.taken_moves) == 1:
			available_moves = [(a, b) for a in range(self._nrows) for b in range(self._ncols)][:-1]
			return list(set(available_moves) - set(self.taken_moves))

		legal_moves = []
		ppx,  ppy   = self.player_positions[self.active_player]
		initial_pos = self.player_positions[self.active_player]

		for direction in self.directions:
			possble = deepcopy(initial_pos)

			while True:
				possble = (possble[0] + direction[0], possble[1] + direction[1])
				if possble in self.board_pos:
					if possble not in self.taken_moves:
						legal_moves.append(possble)
					else:
						break
				else:
					break

		random.shuffle(legal_moves)
		return legal_moves




a = GameState()
b = a.forecast_move((1,1))

