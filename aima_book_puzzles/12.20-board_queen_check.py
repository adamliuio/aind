
import random
import matplotlib.pyplot as plt
from copy import copy
from time import time

queens_positions_str =  "24748552"
queens_positions_strs = ["24748552", "32752411", "32543213", "24415124"]



def main(runTime):

	# for i in queens_positions_strs:
	# 	print(len(board_fitness(i)))
	# attacking_pairs = board_fitness(queens_positions_str)
	# print("there are   %s       attacking pairs in this puzzle." % len(attacking_pairs))
	# print("there are   %s   non-attacking pairs in this puzzle." % (28-len(attacking_pairs)))

	# check fitnesses of strings
	
	total = []
	start = time()
	check = 1
	rounds = 0

	while True:

		rounds += 1
		if time() - start > runTime:
			print("shit's taking too long, and the minimum 1 is: %s, and went %s rounds." % (min(sum(total, [])), rounds))
			break
		if check:
			new_queens_positions_strs = copy(queens_positions_strs)
			check = 0

		fitness_arr = []
		for string in new_queens_positions_strs:
			_, fit = board_fitness(string)
			fitness_arr.append(fit)

		total.append(fitness_arr)

		if 0 in fitness_arr:
			print("SUCCESS!!!")
			print(fitness_arr)
			print(new_queens_positions_strs)
			print("went %s rounds." % rounds)
			trend = [min(ar) for ar in total]
			plt.plot(trend)
			plt.show()
			break

		# get rid of the least fit string
		sorted_sequence = sorted(range(len(fitness_arr)), key=lambda k: fitness_arr[k])
		min_loc = fitness_arr.index(min(fitness_arr))
		del fitness_arr[min_loc]
		del new_queens_positions_strs[min_loc]

		# generate new parents pairs
		new_parent_pairs = generate_new_parent_pairs(new_queens_positions_strs)
		new_queens_positions_strs = parents_have_sex(new_parent_pairs)









#################################################################################################################
######################################  Function List  ##########################################################
#################################################################################################################


def mutation(babies):

	for _ in range(random.randint(1, 4)):
		babyNum = random.randint(0, 3)
		baby = babies[babyNum]

		# if there are repeated elements, direct the mutation to use the elements that are not used
		if len(set(baby)) < 8:
			candidates = list(set("12345678") - set(baby))
			repeated_poses, _ = [], []
			for i in range(len(baby)):
				if baby[i] not in _:
					_.append(baby[i])
				else:
					repeated_poses.append(i)
			repeated_pos = random.choice(repeated_poses)
			babies[babyNum] = baby[:repeated_pos] + random.choice(candidates) + baby[repeated_pos+1:]

		# or if there's none, then choose random ones to mutate
		else:
			char_loc = random.randint(0, 7)
			babies[babyNum] = baby[:char_loc] + str(random.randint(1, 8)) + baby[char_loc+1:]

	return babies

# :param -> list of lists of parents
def parents_have_sex(parents_pairs):

	babies = []
	for pair in parents_pairs:
		split_rate = get_split_rate()
		babies.append(pair[0][:split_rate]+pair[1][split_rate:])
		babies.append(pair[1][:split_rate]+pair[0][split_rate:])

	# do some mutation for them to evolve
	babies = mutation(babies)

	return babies



# :param -> list of parents that without the one with the lowest survival rate
def generate_new_parent_pairs(selected_parents):
	best_parent = selected_parents[0]
	new_parents = []
	for parent in selected_parents[1:]:
		new_parents.append([best_parent, parent])
	return new_parents



def get_split_rate():
	return random.randint(3, 6)



def get_survival_rate(fitness_arr):
	total = sum(fitness_arr)
	return [x / total for x in fitness_arr]



# the board is 100% fit when the function returns 0
def board_fitness(queens_positions_str):

	queen_locs = [(x, int(queens_positions_str[x-1])) for x in range(1, 9)]
	queen_ranges = []
	attacking_pairs = []

	for queen_loc in queen_locs:
		queen_ranges.append(get_queen_range(queen_loc))

	for queen_loc in queen_locs:
		for r in range(len(queen_ranges)):
			if queen_loc in queen_ranges[r]:
				pair = sorted([queen_loc, queen_locs[r]])
				if pair not in attacking_pairs:
					attacking_pairs.append(pair)

	return attacking_pairs, 28-len(attacking_pairs)



def get_queen_range(queen_loc):

	x = queen_loc[0]
	y = queen_loc[1]
	directions = [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1] if (a, b) != (0, 0)]
	queen_range = []

	for d in directions:
		d_x = d[0]
		d_y = d[1]

		while 1 <= x+d_x and x+d_x <= 8 and 1 <= y+d_y and y+d_y <= 8:

			queen_range.append((x+d_x, y+d_y))

			if   d_x < 0: d_x -= 1
			elif d_x > 0: d_x += 1
			if   d_y < 0: d_y -= 1
			elif d_y > 0: d_y += 1

	return queen_range



if __name__ == "__main__":

	main(300)
	# mutation(queens_positions_strs)




































