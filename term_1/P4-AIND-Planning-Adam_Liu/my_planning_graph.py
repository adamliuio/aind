from aimacode.utils import expr
from lp_utils import decode_state
from aimacode.search import Problem
from aimacode.planning import Action



"""
	Base class for planning graph nodes.

	includes instance sets common to both types of nodes used in a planning graph
	parents:  the set of nodes in the previous level
	children: the set of nodes in the subsequent level
	mutex:    the set of sibling nodes that are mutually exclusive with this node
"""
class PgNode():

	def __init__(self):
		self.mutex    = set()
		self.parents  = set()
		self.children = set()


	"""
		Boolean test for mutual exclusion

		:param other: PgNode
			the other node to compare with
		:return: bool
			True if this node and the other are marked mutually exclusive (mutex)
	"""
	def is_mutex(self, other) -> bool:
		if other in self.mutex:
			return True
		return False


	"""
		helper print for debugging shows counts of parents, children, siblings

		:return:
			print only
	"""
	def show(self):
		print("{} parents".format(len(self.parents)))
		print("{} children".format(len(self.children)))
		print("{} mutex".format(len(self.mutex)))


"""
	A planning graph node representing a state (literal fluent) from a
	planning problem.

	Args:
	----------
	symbol : str
		A string representing a literal expression from a planning problem
		domain.

	is_pos : bool
		Boolean flag indicating whether the literal expression is positive or
		negative.
"""
class PgNode_s(PgNode):

	"""
		S-level Planning Graph node constructor

		:param symbol: expr
		:param is_pos: bool

		Instance variables calculated:
			literal: expr
					fluent in its literal form including negative operator if applicable
		Instance variables inherited from PgNode:
			parents:  set of nodes connected to this node in previous A level; initially empty
			children: set of nodes connected to this node in next A level; initially empty
			mutex:    set of sibling S-nodes that this node has mutual exclusion with; initially empty
	"""
	def __init__(self, symbol: str, is_pos: bool):
		PgNode.__init__(self)
		self.symbol = symbol
		self.is_pos = is_pos
		self.__hash = None


	"""
		helper print for debugging shows literal plus counts of parents,
		children, siblings

		:return:
			print only
	"""
	def show(self):
		if self.is_pos: print("\n*** {}".format(self.symbol))
		else:           print("\n*** ~{}".format(self.symbol))
		PgNode.show(self)


	"""
		equality test for nodes - compares only the literal for equality

		:param other: PgNode_s
		:return: bool
	"""
	def __eq__(self, other):
		return (isinstance(other, self.__class__) and
				self.is_pos == other.is_pos and
				self.symbol == other.symbol)


	def __hash__(self):
		self.__hash = self.__hash or hash(self.symbol) ^ hash(self.is_pos)
		return self.__hash



"""
	A-type (action) Planning Graph node - inherited from PgNode
"""
class PgNode_a(PgNode):

	"""
		A-level Planning Graph node constructor

		:param action: Action
			a ground action, i.e. this action cannot contain any variables
		Instance variables calculated:
			An A-level will always have an S-level as its parent and an S-level as its child.
			The preconditions and effects will become the parents and children of the A-level node
			However, when this node is created, it is not yet connected to the graph
			prenodes: set of *possible* parent S-nodes
			effnodes: set of *possible* child S-nodes
			is_persistent: bool   True if this is a persistence action, i.e. a no-op action
		Instance variables inherited from PgNode:
			parents: set of nodes connected to this node in previous S level; initially empty
			children: set of nodes connected to this node in next S level; initially empty
			mutex: set of sibling A-nodes that this node has mutual exclusion with; initially empty
	"""
	def __init__(self, action: Action):
		self.__hash = None
		self.action = action
		self.effnodes = self.effect_s_nodes()
		self.prenodes = self.precond_s_nodes()
		self.is_persistent = self.prenodes == self.effnodes
		PgNode.__init__(self)



	"""
		helper print for debugging shows action plus counts of parents, children, siblings

		:return:
			print only
	"""
	def show(self):
		print("\n*** {!s}".format(self.action))
		PgNode.show(self)



	"""
		precondition literals as S-nodes (represents possible parents for this node).
		It is computationally expensive to call this function; it is only called by the
		class constructor to populate the `prenodes` attribute.

		:return: set of PgNode_s
	"""
	def precond_s_nodes(self):
		nodes = set()
		for p in self.action.precond_pos:
			nodes.add(PgNode_s(p, True))
		for p in self.action.precond_neg:
			nodes.add(PgNode_s(p, False))
		return nodes



	"""
		effect literals as S-nodes (represents possible children for this node).
		It is computationally expensive to call this function; it is only called by the
		class constructor to populate the `effnodes` attribute.

		:return: set of PgNode_s
	"""
	def effect_s_nodes(self):
		nodes = set()
		for e in self.action.effect_add:
			nodes.add(PgNode_s(e, True))
		for e in self.action.effect_rem:
			nodes.add(PgNode_s(e, False))
		return nodes



	"""
		equality test for nodes - compares only the action name for equality

		:param other: PgNode_a
		:return: bool
	"""
	def __eq__(self, other):
		return (isinstance(other, self.__class__) and
				self.is_persistent == other.is_persistent and
				self.action.name   == other.action.name and
				self.action.args   == other.action.args)



	def __hash__(self):
		self.__hash = self.__hash or hash(self.action.name) ^ hash(self.action.args)
		return self.__hash



"""
	adds sibling nodes to each other's mutual exclusion (mutex) set. These should be sibling nodes!

	:param node1: PgNode (or inherited PgNode_a, PgNode_s types)
	:param node2: PgNode (or inherited PgNode_a, PgNode_s types)
	:return:
		node mutex sets modified
"""
def mutexify(node1: PgNode, node2: PgNode):

	if type(node1) != type(node2):
		raise TypeError('Attempted to mutex two nodes of different types')

	node1.mutex.add(node2)
	node2.mutex.add(node1)



"""
	A planning graph as described in chapter 10 of the AIMA text. The planning
	graph can be used to reason about 
"""
class PlanningGraph():

	"""
		:param problem: PlanningProblem (or subclass such as AirCargoProblem or HaveCakeProblem)
		:param state: str (will be in form TFTTFF... representing fluent states)
		:param serial_planning: bool (whether or not to assume that only one action can occur at a time)
		Instance variable calculated:
			fs: FluentState
				the state represented as positive and negative fluent literal lists
			all_actions: list of the PlanningProblem valid ground actions combined with calculated no-op actions
			s_levels: list of sets of PgNode_s, where each set in the list represents an S-level in the planning graph
			a_levels: list of sets of PgNode_a, where each set in the list represents an A-level in the planning graph
	"""
	def __init__(self, problem: Problem, state: str, serial_planning=True):
		self.s_levels    = []
		self.a_levels    = []
		self.problem     = problem
		self.serial      = serial_planning
		self.fs          = decode_state(state, problem.state_map)
		self.all_actions = self.problem.actions_list + self.noop_actions(self.problem.state_map)
		self.create_graph()



	"""
		create persistent action for each possible fluent

		"No-Op" actions are virtual actions (i.e., actions that only exist in
		the planning graph, not in the planning problem domain) that operate
		on each fluent (literal expression) from the problem domain. No op
		actions "pass through" the literal expressions from one level of the
		planning graph to the next.

		The no-op action list requires both a positive and a negative action
		for each literal expression. Positive no-op actions require the literal
		as a positive precondition and add the literal expression as an effect
		in the output, and negative no-op actions require the literal as a
		negative precondition and remove the literal expression as an effect in
		the output.

		This function should only be called by the class constructor.

		:param literal_list:
		:return: list of Action
	"""
	def noop_actions(self, literal_list):

		action_list = []
		for fluent in literal_list:
			act1 = Action(expr("Noop_pos({})".format(fluent)), ([fluent], []), ([fluent], []))
			action_list.append(act1)
			act2 = Action(expr("Noop_neg({})".format(fluent)), ([], [fluent]), ([], [fluent]))
			action_list.append(act2)

		return action_list



	"""
		build a Planning Graph as described in Russell-Norvig 3rd Ed 10.3 or 2nd Ed 11.4

		The S0 initial level has been implemented for you.  It has no parents and includes all of
		the literal fluents that are part of the initial state passed to the constructor.  At the start
		of a problem planning search, this will be the same as the initial state of the problem.  However,
		the planning graph can be built from any state in the Planning Problem

		This function should only be called by the class constructor.

		:return:
			builds the graph by filling s_levels[] and a_levels[] lists with node sets for each level
	"""
	def create_graph(self):

		# the graph should only be built during class construction
		if (len(self.s_levels) != 0) or (len(self.a_levels) != 0):
			raise Exception('Planning Graph already created; construct a new planning graph for each new state in the planning sequence')

		# initialize S0 to literals in initial state provided.
		level   = 0
		leveled = False
		self.s_levels.append(set())  # S0 set of s_nodes - empty to start
		# for each fluent in the initial state, add the correct literal PgNode_s
		for literal in self.fs.pos:
			self.s_levels[level].add(PgNode_s(literal, True))
		for literal in self.fs.neg:
			self.s_levels[level].add(PgNode_s(literal, False))
		# no mutexes at the first level

		# continue to build the graph alternating A, S levels until last two S levels contain the same literals,
		# i.e. until it is "leveled"
		while not leveled:
			self.add_action_level(level)
			self.update_a_mutex(self.a_levels[level])

			level += 1
			self.add_literal_level(level)
			self.update_s_mutex(self.s_levels[level])

			if self.s_levels[level] == self.s_levels[level - 1]:
				leveled = True



	"""
		add an A (action) level to the Planning Graph

		:param level: int
			the level number alternates S0, A0, S1, A1, S2, .... etc the level number is also used as the
			index for the node set lists self.a_levels[] and self.s_levels[]
		:return:
			adds A nodes to the current level in self.a_levels[level]
	"""
	def add_action_level(self, level):

		actions          = self.all_actions
		previous_s_level = self.s_levels[level]
		self.a_levels.append(set())

		for action in actions:
			a_node = PgNode_a(action)

			# 1. determine what actions to add and create those PgNode_a objects
			if a_node.prenodes.issubset(previous_s_level):

				# 2. connect the nodes to the previous S literal level
				for s_node in previous_s_level:
					s_node.children.add(a_node)
					a_node.parents.add(s_node)

				self.a_levels[level].add(a_node)


	"""
		add an S (literal) level to the Planning Graph

		:param level: int
			the level number alternates S0, A0, S1, A1, S2, .... etc the level number is also used as the
			index for the node set lists self.a_levels[] and self.s_levels[]
		:return:
			adds S nodes to the current level in self.s_levels[level]
	"""
	def add_literal_level(self, level):

		previous_a_level = self.a_levels[level - 1]
		self.s_levels.append(set())

		# 1. determine what literals to add
		for a_node in previous_a_level:
			for effect_node in a_node.effnodes:

				# 2. connect the nodes
				a_node.children.add(effect_node)
				effect_node.parents.add(a_node)
				self.s_levels[level].add(effect_node)


	"""
		Determine and update sibling mutual exclusion for A-level nodes

		Mutex action tests section from 3rd Ed. 10.3 or 2nd Ed. 11.4
		A mutex relation holds between two actions a given level
		if the planning graph is a serial planning graph and the pair are nonpersistence actions
		or if any of the three conditions hold between the pair:
		   Inconsistent Effects
		   Interference
		   Competing needs

		:param nodeset: set of PgNode_a (siblings in the same level)
		:return:
			mutex set in each PgNode_a in the set is appropriately updated
	"""
	def update_a_mutex(self, nodeset):
		nodelist = list(nodeset)
		for i, n1 in enumerate(nodelist[:-1]):
			for n2 in nodelist[i + 1:]:
				if (self.serialize_actions(n1, n2) or
						self.inconsistent_effects_mutex(n1, n2) or
						self.interference_mutex(n1, n2) or
						self.competing_needs_mutex(n1, n2)):
					mutexify(n1, n2)



	"""
		Test a pair of actions for mutual exclusion, returning True if the
		planning graph is serial, and if either action is persistent; otherwise
		return False.  Two serial actions are mutually exclusive if they are
		both non-persistent.

		:param node_a1: PgNode_a
		:param node_a2: PgNode_a
		:return: bool
	"""
	def serialize_actions(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
		#
		if not self.serial:
			return False
		if node_a1.is_persistent or node_a2.is_persistent:
			return False
		return True



	"""
		Test a pair of actions for inconsistent effects, returning True if
		one action negates an effect of the other, and False otherwise.

		HINT: The Action instance associated with an action node is accessible
		through the PgNode_a.action attribute. See the Action class
		documentation for details on accessing the effects and preconditions of
		an action.

		:param node_a1: PgNode_a
		:param node_a2: PgNode_a
		:return: bool
	"""
	def inconsistent_effects_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:

		# test for Inconsistent Effects between nodes
		a1_a2_unique = set(node_a1.action.effect_add) & set(node_a2.action.effect_rem)
		a2_a1_unique = set(node_a2.action.effect_add) & set(node_a1.action.effect_rem)

		return bool(a1_a2_unique | a2_a1_unique)



	"""
		Test a pair of actions for mutual exclusion, returning True if the 
		effect of one action is the negation of a precondition of the other.

		HINT: The Action instance associated with an action node is accessible
		through the PgNode_a.action attribute. See the Action class
		documentation for details on accessing the effects and preconditions of
		an action.

		:param node_a1: PgNode_a
		:param node_a2: PgNode_a
		:return: bool
	"""
	def interference_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:

		# test for Interference between nodes
		mutex = set(node_a1.action.effect_add) & set(node_a2.action.precond_neg) | \
				set(node_a1.action.effect_rem) & set(node_a2.action.precond_pos) | \
				set(node_a2.action.effect_add) & set(node_a1.action.precond_neg) | \
				set(node_a2.action.effect_rem) & set(node_a1.action.precond_pos)

		return bool(mutex)



	"""
		Test a pair of actions for mutual exclusion, returning True if one of
		the precondition of one action is mutex with a precondition of the
		other action.

		:param node_a1: PgNode_a
		:param node_a2: PgNode_a
		:return: bool
	"""
	def competing_needs_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:

		# test for Competing Needs between nodes
		for a1_parent in node_a1.parents:
			for a2_parent in node_a2.parents:

				if a1_parent.is_mutex(a2_parent):
					return True

		return False



	"""
		Determine and update sibling mutual exclusion for S-level nodes

		Mutex action tests section from 3rd Ed. 10.3 or 2nd Ed. 11.4
		A mutex relation holds between literals at a given level
		if either of the two conditions hold between the pair:
		   Negation
		   Inconsistent support

		:param nodeset: set of PgNode_a (siblings in the same level)
		:return:
			mutex set in each PgNode_a in the set is appropriately updated
	"""
	def update_s_mutex(self, nodeset: set):
		nodelist = list(nodeset)
		for i, n1 in enumerate(nodelist[:-1]):
			for n2 in nodelist[i + 1:]:
				if self.negation_mutex(n1, n2) or self.inconsistent_support_mutex(n1, n2):
					mutexify(n1, n2)



	"""
		Test a pair of state literals for mutual exclusion, returning True if
		one node is the negation of the other, and False otherwise.

		HINT: Look at the PgNode_s.__eq__ defines the notion of equivalence for
		literal expression nodes, and the class tracks whether the literal is
		positive or negative.

		:param node_s1: PgNode_s
		:param node_s2: PgNode_s
		:return: bool
	"""
	def negation_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s) -> bool:

		# test for negation between nodes
		is_same_symbol = node_s1.symbol == node_s2.symbol
		is_negation    = node_s1.is_pos != node_s2.is_pos
		mutual_exclusion = is_same_symbol and is_negation

		return mutual_exclusion



	"""
		Test a pair of state literals for mutual exclusion, returning True if
		there are no actions that could achieve the two literals at the same
		time, and False otherwise.  In other words, the two literal nodes are
		mutex if all of the actions that could achieve the first literal node
		are pairwise mutually exclusive with all of the actions that could
		achieve the second literal node.

		HINT: The PgNode.is_mutex method can be used to test whether two nodes
		are mutually exclusive.

		:param node_s1: PgNode_s
		:param node_s2: PgNode_s
		:return: bool
	"""
	def inconsistent_support_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s):

		# test for Inconsistent Support between nodes
		for s1_parent in node_s1.parents:
			for s2_parent in node_s2.parents:

				if not s1_parent.is_mutex(s2_parent):
					return False

		return True



	"""
		The sum of the level costs of the individual goals (admissible if goals independent)
		:return: int
	"""
	def h_levelsum(self) -> int:

		level_sum = 0

		for goal in self.problem.goal:
			node = PgNode_s(goal, True)
			s_levels_list = enumerate(self.s_levels)

			for level, s_nodes in s_levels_list:
				
				if node in s_nodes:
					level_sum += level
					break

		return level_sum



