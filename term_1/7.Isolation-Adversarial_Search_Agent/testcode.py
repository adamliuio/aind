
#########################
# test `minimax_helpers`
#########################

print("\ntesting `minimax_helpers`\n")

import minimax_helpers

from gamestate import *

g = GameState()

print("Calling min_value on an empty board...")
v = minimax_helpers.min_value(g)

if v == -1:
	print("min_value() returned the expected score!")
else:
	print("Uh oh! min_value() did not return the expected score.")





#########################
# test `minimax_decision`
#########################

print("\ntesting `minimax_decision`\n")

import minimax
import gamestate as game


best_moves = set([(0, 0), (2, 0), (0, 1)])
rootNode = game.GameState()
minimax_move = minimax.minimax_decision(rootNode)

print("Best move choices: {}".format(list(best_moves)))
print("Your code chose: {}".format(minimax_move))

if minimax_move in best_moves:
    print("That's one of the best move choices. Looks like your minimax-decision function worked!")
else:
    print("Uh oh...looks like there may be a problem.")
