# NOTE: This function is provided for reference; it is not imported or used
# by the test code when you submit (this allows for dependency isolation
# in the test cases)

import minimax_helpers

from gamestate import *
from time import time

start = time()

g = GameState()

print("Calling min_value on an empty board...")
v = minimax_helpers.min_value(g)

if v == -1:
	print("min_value() returned the expected score!")
else:
	print("Uh oh! min_value() did not return the expected score.")

print(time() - start)