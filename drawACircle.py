


def main():

	# draw the circle
	









def drawAtLoc(loc):
	s = list(canvas[loc[0]])
	s[loc[1]] = "O"
	canvas[loc[0]] = "".join(s)


def printCanvas():
	for r in canvas:
		print(r)

# defining canvas with a starting point
row = "................................................................................................"
canvas = [row] * 45
starting_point = (8, 47)
drawAtLoc(starting_point)


if __name__ == "__main__":
	main()