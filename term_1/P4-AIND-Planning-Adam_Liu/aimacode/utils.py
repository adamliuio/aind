"""
	Provides some utilities widely used by other modules
"""

import math
import heapq
import bisect
import random
import os.path
import operator
import functools
import collections
import collections.abc

from collections import defaultdict

# ______________________________________________________________________________
# Functions on Sequences and Iterables


def sequence(iterable):
	"Coerce iterable to sequence, if it is not already one."
	return (iterable if isinstance(iterable, collections.abc.Sequence)
			else tuple(iterable))


def removeall(item, seq):
	"""Return a copy of seq (or string) with all occurences of item removed."""
	if isinstance(seq, str):
		return seq.replace(item, '')
	else:
		return [x for x in seq if x != item]


def unique(seq):  # TODO: replace with set
	"""Remove duplicate elements from seq. Assumes hashable elements."""
	return list(set(seq))


def count(seq):
	"""Count the number of items in sequence that are interpreted as true."""
	return sum(bool(x) for x in seq)


def product(numbers):
	"""Return the product of the numbers, e.g. product([2, 3, 10]) == 60"""
	result = 1
	for x in numbers:
		result *= x
	return result


def first(iterable, default=None):
	"Return the first element of an iterable or the next element of a generator; or default."
	try:
		return iterable[0]
	except IndexError:
		return default
	except TypeError:
		return next(iterable, default)


def is_in(elt, seq):
	"""Similar to (elt in seq), but compares with 'is', not '=='."""
	return any(x is elt for x in seq)

# ______________________________________________________________________________
# argmin and argmax

identity = lambda x: x

argmin = min
argmax = max


"""
	Return a minimum element of seq; break ties at random.
"""
def argmin_random_tie(seq, key=identity):
	return argmin(shuffled(seq), key=key)


def argmax_random_tie(seq, key=identity):
	"Return an element with highest fn(seq[i]) score; break ties at random."
	return argmax(shuffled(seq), key=key)


def shuffled(iterable):
	"Randomly shuffle a copy of iterable."
	items = list(iterable)
	random.shuffle(items)
	return items



# ______________________________________________________________________________
# Statistical and mathematical functions


"""
	Return a list of (value, count) pairs, summarizing the input values.
	Sorted by increasing value, or if mode=1, by decreasing count.
	If bin_function is given, map it over values first.
"""
def histogram(values, mode=0, bin_function=None):
	if bin_function:
		values = map(bin_function, values)

	bins = {}
	for val in values:
		bins[val] = bins.get(val, 0) + 1

	if mode:
		return sorted(list(bins.items()), key=lambda x: (x[1], x[0]),
					  reverse=True)
	else:
		return sorted(bins.items())


"""
	Return the sum of the element-wise product of vectors X and Y.
"""
def dotproduct(X, Y):
	return sum(x * y for x, y in zip(X, Y))


"""
	Return vector as an element-wise product of vectors X and Y
"""
def element_wise_product(X, Y):
	assert len(X) == len(Y)
	return [x * y for x, y in zip(X, Y)]


"""
	Return a matrix as a matrix-multiplication of X_M and arbitary number of matrices *Y_M
"""
def matrix_multiplication(X_M, *Y_M):

	"""
		Return a matrix as a matrix-multiplication of two matrices X_M and Y_M
		>>> matrix_multiplication([[1, 2, 3],
								   [2, 3, 4]],
								   [[3, 4],
									[1, 2],
									[1, 0]])
		[[8, 8],[13, 14]]
	"""
	def _mat_mult(X_M, Y_M):

		assert len(X_M[0]) == len(Y_M)

		result = [[0 for i in range(len(Y_M[0]))] for j in range(len(X_M))]
		for i in range(len(X_M)):
			for j in range(len(Y_M[0])):
				for k in range(len(Y_M)):
					result[i][j] += X_M[i][k] * Y_M[k][j]
		return result

	result = X_M

	for Y in Y_M:
		result = _mat_mult(result, Y)

	return result


"""
	Converts a vector to a diagonal matrix with vector elements
	as the diagonal elements of the matrix
"""
def vector_to_diagonal(v):
	diag_matrix = [[0 for i in range(len(v))] for j in range(len(v))]
	for i in range(len(v)):
		diag_matrix[i][i] = v[i]

	return diag_matrix


def vector_add(a, b):
	"""Component-wise addition of two vectors."""
	return tuple(map(operator.add, a, b))



def scalar_vector_product(X, Y):
	"""Return vector as a product of a scalar and a vector"""
	return [X * y for y in Y]


def scalar_matrix_product(X, Y):
	return [scalar_vector_product(X, y) for y in Y]


def inverse_matrix(X):
	"""Inverse a given square matrix of size 2x2"""
	assert len(X) == 2
	assert len(X[0]) == 2
	det = X[0][0] * X[1][1] - X[0][1] * X[1][0]
	assert det != 0
	inv_mat = scalar_matrix_product(1.0/det, [[X[1][1], -X[0][1]], [-X[1][0], X[0][0]]])

	return inv_mat


def probability(p):
	"Return true with probability p."
	return p > random.uniform(0.0, 1.0)


"""
	Pick n samples from seq at random, with replacement, with the
	probability of each element in proportion to its corresponding
	weight.
"""
def weighted_sample_with_replacement(seq, weights, n):
	sample = weighted_sampler(seq, weights)

	return [sample() for _ in range(n)]


def weighted_sampler(seq, weights):
	"Return a random-sample function that picks from seq weighted by weights."
	totals = []
	for w in weights:
		totals.append(w + totals[-1] if totals else w)

	return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]


def rounder(numbers, d=4):
	"Round a single number, or sequence of numbers, to d decimal places."
	if isinstance(numbers, (int, float)):
		return round(numbers, d)
	else:
		constructor = type(numbers)     # Can be list, set, tuple, etc.
		return constructor(rounder(n, d) for n in numbers)


"""
	The argument is a string; convert to a number if
	possible, or strip it.
"""
def num_or_str(x):
	try:
		return int(x)
	except ValueError:
		try:
			return float(x)
		except ValueError:
			return str(x).strip()


def normalize(dist):
	"""Multiply each number by a constant such that the sum is 1.0"""
	if isinstance(dist, dict):
		total = sum(dist.values())
		for key in dist:
			dist[key] = dist[key] / total
			assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
		return dist
	total = sum(dist)
	return [(n / total) for n in dist]


def clip(x, lowest, highest):
	"""Return x clipped to the range [lowest..highest]."""
	return max(lowest, min(x, highest))


def sigmoid(x):
	"""Return activation value of x with sigmoid function"""
	return 1/(1 + math.exp(-x))


def step(x):
	"""Return activation value of x with sign function"""
	return 1 if x >= 0 else 0

try:  # math.isclose was added in Python 3.5; but we might be in 3.4
	from math import isclose
except ImportError:
	def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
		"Return true if numbers a and b are close to each other."
		return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# ______________________________________________________________________________
# Misc Functions


# TODO: Use functools.lru_cache memoization decorator


def memoize(fn, slot=None):
	"""Memoize fn: make it remember the computed value for any argument list.
	If slot is specified, store result in that slot of first argument.
	If slot is false, store results in a dictionary."""
	if slot:
		def memoized_fn(obj, *args):
			if hasattr(obj, slot):
				return getattr(obj, slot)
			else:
				val = fn(obj, *args)
				setattr(obj, slot, val)
				return val
	else:
		def memoized_fn(*args):
			if args not in memoized_fn.cache:
				memoized_fn.cache[args] = fn(*args)
			return memoized_fn.cache[args]

		memoized_fn.cache = {}

	return memoized_fn


def name(obj):
	"Try to find some reasonable name for the object."
	return (getattr(obj, 'name', 0) or getattr(obj, '__name__', 0) or
			getattr(getattr(obj, '__class__', 0), '__name__', 0) or
			str(obj))


def isnumber(x):
	"Is x a number?"
	return hasattr(x, '__int__')


def issequence(x):
	"Is x a sequence?"
	return isinstance(x, collections.abc.Sequence)


def print_table(table, header=None, sep='   ', numfmt='%g'):
	"""Print a list of lists as a table, so that columns line up nicely.
	header, if specified, will be printed as the first row.
	numfmt is the format for all numbers; you might want e.g. '%6.2f'.
	(If you want different formats in different columns,
	don't use print_table.) sep is the separator between columns."""
	justs = ['rjust' if isnumber(x) else 'ljust' for x in table[0]]

	if header:
		table.insert(0, header)

	table = [[numfmt.format(x) if isnumber(x) else x for x in row]
			 for row in table]

	sizes = list(
			map(lambda seq: max(map(len, seq)),
				list(zip(*[map(str, row) for row in table]))))

	for row in table:
		print(sep.join(getattr(
			str(x), j)(size) for (j, size, x) in zip(justs, sizes, row)))


def AIMAFile(components, mode='r'):
	"Open a file based at the AIMA root directory."
	aima_root = os.path.dirname(__file__)

	aima_file = os.path.join(aima_root, *components)

	return open(aima_file)


def DataFile(name, mode='r'):
	"Return a file in the AIMA /aimacode-data directory."
	return AIMAFile(['aimacode-data', name], mode)


# ______________________________________________________________________________
# Expressions

# See https://docs.python.org/3/reference/expressions.html#operator-precedence
# See https://docs.python.org/3/reference/datamodel.html#special-method-names

"""
	A mathematical expression with an operator and 0 or more arguments.
	op is a str like '+' or 'sin'; args are Expressions.
	Expr('x') or Symbol('x') creates a symbol (a nullary Expr).
	Expr('-', x) creates a unary; Expr('+', x, 1) creates a binary.
"""
class Expr(object):

	def __init__(self, op, *args):
		self.op = str(op)
		self.args = args
		self.__hash = None

	# Operator overloads
	def __neg__(self):           return Expr('-',  self)
	def __pos__(self):           return Expr('+',  self)
	def __invert__(self):        return Expr('~',  self)
	def __add__(self, rhs):      return Expr('+',  self, rhs)
	def __sub__(self, rhs):      return Expr('-',  self, rhs)
	def __mul__(self, rhs):      return Expr('*',  self, rhs)
	def __pow__(self, rhs):      return Expr('**', self, rhs)
	def __mod__(self, rhs):      return Expr('%',  self, rhs)
	def __and__(self, rhs):      return Expr('&',  self, rhs)
	def __xor__(self, rhs):      return Expr('^',  self, rhs)
	def __rshift__(self, rhs):   return Expr('>>', self, rhs)
	def __lshift__(self, rhs):   return Expr('<<', self, rhs)
	def __truediv__(self, rhs):  return Expr('/',  self, rhs)
	def __floordiv__(self, rhs): return Expr('//', self, rhs)
	def __matmul__(self, rhs):   return Expr('@',  self, rhs)

	"""
		Allow both P | Q, and P |'==>'| Q.
	"""
	def __or__(self, rhs):
		if isinstance(rhs, Expression):
			return Expr('|', self, rhs)
		else:
			return PartialExpr(rhs, self)

	# Reverse operator overloads
	def __ror__(self, lhs):       return Expr('|',  lhs, self)
	def __radd__(self, lhs):      return Expr('+',  lhs, self)
	def __rsub__(self, lhs):      return Expr('-',  lhs, self)
	def __rmul__(self, lhs):      return Expr('*',  lhs, self)
	def __rdiv__(self, lhs):      return Expr('/',  lhs, self)
	def __rpow__(self, lhs):      return Expr('**', lhs, self)
	def __rmod__(self, lhs):      return Expr('%',  lhs, self)
	def __rand__(self, lhs):      return Expr('&',  lhs, self)
	def __rxor__(self, lhs):      return Expr('^',  lhs, self)
	def __rmatmul__(self, lhs):   return Expr('@',  lhs, self)
	def __rrshift__(self, lhs):   return Expr('>>', lhs, self)
	def __rlshift__(self, lhs):   return Expr('<<', lhs, self)
	def __rtruediv__(self, lhs):  return Expr('/',  lhs, self)
	def __rfloordiv__(self, lhs): return Expr('//', lhs, self)

	def __call__(self, *args):
		"Call: if 'f' is a Symbol, then f(0) == Expr('f', 0)."
		if self.args:
			raise ValueError('can only do a call for a Symbol, not an Expr')
		else:
			return Expr(self.op, *args)

	# Equality and repr
	def __eq__(self, other):
		"'x == y' evaluates to True or False; does not build an Expr."
		return (isinstance(other, Expr)
				and self.op   == other.op
				and self.args == other.args)

	def __hash__(self):
		self.__hash = self.__hash or hash(self.op) ^ hash(self.args)
		return self.__hash

	def __repr__(self):
		op = self.op
		args = [str(arg) for arg in self.args]

		# f(x) or f(x, y)
		if op.isidentifier():
			return '{}({})'.format(op, ', '.join(args)) if args else op
		# -x or -(x + 1)
		elif len(args) == 1:
			return op + args[0]
		# (x - y)
		else:
			opp = (' ' + op + ' ')
			return '(' + opp.join(args) + ')'


# An 'Expression' is either an Expr or a Number.
# Symbol is not an explicit type; it is any Expr with 0 args.

Number     = (int, float, complex)
Expression = (Expr, Number)


def Symbol(name):
	"A Symbol is just an Expr with no args."
	return Expr(name)


def symbols(names):
	"Return a tuple of Symbols; names is a comma/whitespace delimited str."
	return tuple(Symbol(name) for name in names.replace(',', ' ').split())


def subexpressions(x):
	"Yield the subexpressions of an Expression (including x itself)."
	yield x
	if isinstance(x, Expr):
		for arg in x.args:
			yield from subexpressions(arg)


def arity(expression):
	"The number of sub-expressions in this expression."
	if isinstance(expression, Expr):
		return len(expression.args)
	else:  # expression is a number
		return 0

# For operators that are not defined in Python, we allow new InfixOps:


"""
	Given 'P |'==>'| Q, first form PartialExpr('==>', P), then combine with Q.
"""
class PartialExpr:

	def __init__(self, op, lhs): self.op, self.lhs = op, lhs
	def __or__(self, rhs):       return Expr(self.op, self.lhs, rhs)
	def __repr__(self):          return "PartialExpr('{}', {})".format(self.op, self.lhs)


"""
	Shortcut to create an Expression. x is a str in which:
	- identifiers are automatically defined as Symbols.
	- ==> is treated as an infix |'==>'|, as are <== and <=>.
	If x is already an Expression, it is returned unchanged. Example:
	>>> expr('P & Q ==> Q')
	((P & Q) ==> Q)
"""
def expr(x):
	if isinstance(x, str):
		return eval(expr_handle_infix_ops(x), defaultkeydict(Symbol))
	else:
		return x

infix_ops = '==> <== <=>'.split()


"""
	Given a str, return a new str with ==> replaced by |'==>'|, etc.
	>>> expr_handle_infix_ops('P ==> Q')
	"P |'==>'| Q"
"""
def expr_handle_infix_ops(x):
	for op in infix_ops:
		x = x.replace(op, '|' + repr(op) + '|')
	return x


"""
	Like defaultdict, but the default_factory is a function of the key.
	>>> d = defaultkeydict(len); d['four']
	4
"""
class defaultkeydict(collections.defaultdict):
	def __missing__(self, key):
		self[key] = result = self.default_factory(key)
		return result


# ______________________________________________________________________________
# Queues: Stack, FIFOQueue, PriorityQueue

# TODO: Possibly use queue.Queue, queue.PriorityQueue
# TODO: Priority queues may not belong here -- see treatment in search.py



"""
	Queue is an abstract class/interface. There are three types:
		Stack(): A Last In First Out Queue.
		FIFOQueue(): A First In First Out Queue.
		PriorityQueue(order, f): Queue in sorted order (default min-first).
	Each type supports the following methods and functions:
		q.append(item)  -- add an item to the queue
		q.extend(items) -- equivalent to: for item in items: q.append(item)
		q.pop()         -- return the top item from the queue
		len(q)          -- number of items in q (also q.__len())
		item in q       -- does q contain item?
	Note that isinstance(Stack(), Queue) is false, because we implement stacks
	as lists.  If Python ever gets interfaces, Queue will be an interface.
"""
class Queue:

	def __init__(self):
		raise NotImplementedError

	def extend(self, items):
		for item in items:
			self.append(item)


def Stack():
	"""Return an empty list, suitable as a Last-In-First-Out Queue."""
	return []


"""
	A First-In-First-Out Queue.
"""
class FIFOQueue(Queue):

	def __init__(self):
		self.A = []
		self.start = 0

	def append(self, item):
		self.A.append(item)

	def __len__(self):
		return len(self.A) - self.start

	def extend(self, items):
		self.A.extend(items)

	def pop(self):
		e = self.A[self.start]
		self.start += 1
		if self.start > 5 and self.start > len(self.A) / 2:
			self.A = self.A[self.start:]
			self.start = 0
		return e

	def __contains__(self, item):
		return item in self.A[self.start:]


"""
	A queue in which the minimum element (as determined by f and
	order) is returned first.  Also supports dict-like lookup.

	MODIFIED FROM AIMA VERSION
		- Use heapq
		- Use an additional dict to track membership
		- remove __delitem__ (AIMA version contains error)
"""
class PriorityQueue(Queue):

	def __init__(self, order=None, f=lambda x: x):
		self.A = []
		self._A = defaultdict(lambda: 0)
		self.f = f

	def append(self, item):
		heapq.heappush(self.A, (self.f(item), item))
		self._A[item] += 1

	def __len__(self):
		return len(self.A)

	def pop(self):
		_, item = heapq.heappop(self.A)
		self._A[item] -= 1
		return item

	def __contains__(self, item):
		return self._A[item] > 0

	def __getitem__(self, key):
		if self._A[key] > 0:
			return key

# ______________________________________________________________________________
# Useful Shorthands


"""
	Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'
"""
class Bool(int):
	__str__ = __repr__ = lambda self: 'T' if self else 'F'

T = Bool(True)
F = Bool(False)

