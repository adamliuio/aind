# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*
	Go through each unit in the unit list, if there are two boxes in an unit containing the same 2 possible values, then we have a pair naked twins. Any other unsolved peer of those 2 boxes in the same unit, if any of their possible values is one of the twins' possible values, we eliminate the digit from the peer's possible values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*
	The original unit groups in the previous exercises only include the peer units in the same column/row/sub-square of a box, to solve the diagonal sudoku problem, we include the peers of a box on the diagonal axes as well, if the box is on a diagonal axis.
	And then, we propagate through the constrained scenarios.