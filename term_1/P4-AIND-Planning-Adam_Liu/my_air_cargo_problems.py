from functools import lru_cache
from aimacode.utils import expr
from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (Node, Problem)
from my_planning_graph import PlanningGraph
from lp_utils import (FluentState, encode_state, decode_state)



"""
		:param cargos: list of str
				cargos in the problem

		:param planes: list of str
				planes in the problem

		:param airports: list of str
				airports in the problem

		:param initial: FluentState object
				positive and negative literal fluents (as expr) describing initial state

		:param goal: list of expr
				literal fluents required for goal test
"""
class AirCargoProblem(Problem):

	def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
		self.cargos           = cargos
		self.planes           = planes
		self.airports         = airports
		self.actions_list     = self.get_actions()
		self.state_map        = initial.pos + initial.neg
		self.initial_state_TF = encode_state(initial, self.state_map)
		Problem.__init__(self, self.initial_state_TF, goal=goal)


	"""
		This method creates concrete actions (no variables) for all actions in the problem
		domain action schema and turns them into complete Action objects as defined in the
		aimacode.planning module. It is computationally expensive to call this method directly;
		however, it is called in the constructor and the results cached in the `actions_list` property.

		Returns:
		----------
		list<Action>
			list of Action objects
	"""
	# TODO create concrete Action objects based on the domain action schema for: Load, Unload, and Fly
	# concrete actions definition: specific literal action that does not include variables as with the schema
	# for example, the action schema 'Load(c, p, a)' can represent the concrete actions 'Load(C1, P1, SFO)'
	# or 'Load(C2, P2, JFK)'. The actions for the planning problem must be concrete because the problems in
	# forward search and Planning Graphs must use Propositional Logic
	def get_actions(self):

		"""
			Create all concrete Load actions and return a list
			:return: list of Action objects
		"""
		def load_actions():

			loads = []

			# create all load ground actions from the domain Load action
			for cargo in self.cargos:
				for plane in self.planes:
					for airport in self.airports:

						precond_pos = [expr("At({}, {})".format(cargo, airport)),
									   expr("At({}, {})".format(plane, airport))]
						precond_neg = []
						effect_add  = [expr("In({}, {})".format(cargo,   plane))]
						effect_rem  = [expr("At({}, {})".format(cargo, airport))]

						load = Action(
							expr("Load({}, {}, {})".format(cargo, plane, airport)),
							[precond_pos, precond_neg],
							[effect_add, effect_rem]
						)

						loads.append(load)

			return loads


		"""
			Create all concrete Unload actions and return a list
			:return: list of Action objects
		"""
		def unload_actions():

			unloads = []

			# create all Unload ground actions from the domain Unload action
			for cargo in self.cargos:
				for plane in self.planes:
					for airport in self.airports:

						precond_pos = [expr("In({}, {})".format(cargo,   plane)),
									   expr("At({}, {})".format(plane, airport))]
						precond_neg = []
						effect_add  = [expr("At({}, {})".format(cargo, airport))]
						effect_rem  = [expr("In({}, {})".format(cargo, plane))]

						unload = Action(
							expr("Unload({}, {}, {})".format(cargo, plane, airport)),
							[precond_pos, precond_neg],
							[effect_add, effect_rem]
						)

						unloads.append(unload)

			return unloads


		"""
			Create all concrete Fly actions and return a list
			:return: list of Action objects
		"""
		def fly_actions():

			flys = []
			for fr in self.airports:
				for to in self.airports:
					if fr != to:
						for p in self.planes:

							precond_pos = [expr("At({}, {})".format(p, fr))]
							precond_neg = []
							effect_add  = [expr("At({}, {})".format(p, to))]
							effect_rem  = [expr("At({}, {})".format(p, fr))]
							fly = Action(
								expr("Fly({}, {}, {})".format(p, fr, to)),
								[precond_pos, precond_neg],
								[effect_add,  effect_rem]
							)

							flys.append(fly)

			return flys


		return load_actions() + unload_actions() + fly_actions()


	"""
		Return the actions that can be executed in the given state.

		:param state: str
			state represented as T/F string of mapped fluents (state variables)
			e.g. 'FTTTFF'
		:return: list of Action objects
	"""
	def actions(self, state: str) -> list:

		kb = PropKB()
		possible_actions = []
		kb.tell(decode_state(state, self.state_map).pos_sentence())

		for action in self.actions_list:

			is_action_possible = True

			for c in action.precond_neg:
				if c in kb.clauses:
					is_action_possible = False
					break

			if is_action_possible:
				if len(list(set(action.precond_pos) - set(kb.clauses))) > 0:
					is_action_possible = False

			if is_action_possible:
				possible_actions.append(action)

		return possible_actions


	"""
		Return the state that results from executing the given
		action in the given state. The action must be one of
		self.actions(state).

		:param state: state entering node
		:param action: Action applied
		:return: resulting state after action
	"""
	def result(self, state: str, action: Action):

		new_state = FluentState([], [])
		old_state = decode_state(state, self.state_map)

		for unique_fluent in list(set(old_state.pos) - set(action.effect_rem)):
			new_state.pos.append(unique_fluent)

		for unique_fluent in list(set(old_state.neg) - set(action.effect_add)):
			new_state.neg.append(unique_fluent)
				
		for unique_fluent in list(set(action.effect_add) - set(new_state.pos)):
			new_state.pos.append(unique_fluent)
				
		for unique_fluent in list(set(action.effect_rem) - set(new_state.neg)):
			new_state.neg.append(unique_fluent)

		return encode_state(new_state, self.state_map)


	"""
		Test the state to see if goal is reached

		:param state: str representing state
		:return: bool
	"""
	def goal_test(self, state: str) -> bool:

		kb = PropKB()
		kb.tell(decode_state(state, self.state_map).pos_sentence())
		if len(list(set(self.goal) - set(kb.clauses))) > 0:
			return False

		# # original
		# for clause in self.goal:
		# 	if clause not in kb.clauses:
		# 		return False

		return True


	def h_1(self, node: Node):
		# note that this is not a true heuristic
		h_const = 1
		return h_const


	"""
		This heuristic uses a planning graph representation of the problem
		state space to estimate the sum of all actions that must be carried
		out from the current state in order to satisfy each individual goal
		condition.
	"""
	@lru_cache(maxsize=8192)
	def h_pg_levelsum(self, node: Node):

		# requires implemented PlanningGraph class
		pg = PlanningGraph(self, node.state)
		pg_levelsum = pg.h_levelsum()

		return pg_levelsum


	"""
		This heuristic estimates the minimum number of actions that must be
		carried out from the current state in order to satisfy all of the goal
		conditions by ignoring the preconditions required for an action to be
		executed.
	"""
	@lru_cache(maxsize=8192)
	def h_ignore_preconditions(self, node: Node):

		kb = PropKB()
		kb.tell(decode_state(node.state, self.state_map).pos_sentence())

		actions_count = 0
		for clause in self.goal:
			if clause not in kb.clauses:
				actions_count += 1
		return actions_count



def air_cargo_p1() -> AirCargoProblem:
	cargos   = ['C1',   'C2']
	planes   = ['P1',   'P2']
	airports = ['JFK', 'SFO']
	pos = [
		expr('At(C1, SFO)'), expr('At(C2, JFK)'),
		expr('At(P1, SFO)'), expr('At(P2, JFK)')
	]
	neg = [
		expr('At(C2, SFO)'), expr('In(C2, P1)'), expr('In(C2, P2)'),
		expr('At(C1, JFK)'), expr('In(C1, P1)'), expr('In(C1, P2)'),
		expr('At(P1, JFK)'), expr('At(P2, SFO)')
	]
	init = FluentState(pos, neg)
	goal = [
		expr('At(C1, JFK)'),
		expr('At(C2, SFO)')
	]
	return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:

	cargos   = [ 'C1',  'C2',  'C3']
	planes   = [ 'P1',  'P2',  'P3']
	airports = ['JFK', 'SFO', 'ATL']
	pos = [
		expr('At(C1, SFO)'), expr('At(C2, JFK)'), expr('At(C3, ATL)'),
		expr('At(P1, SFO)'), expr('At(P2, JFK)'), expr('At(P3, ATL)')
	]
	neg = [
		expr('At(C1, JFK)'), expr('At(C1, ATL)'), expr('In(C1, P1)'), expr('In(C1, P2)'), expr('In(C1, P3)'),
		expr('At(C2, SFO)'), expr('At(C2, ATL)'), expr('In(C2, P1)'), expr('In(C2, P2)'), expr('In(C2, P3)'),
		expr('At(C3, SFO)'), expr('At(C3, JFK)'), expr('In(C3, P1)'), expr('In(C3, P2)'), expr('In(C3, P3)'),
		expr('At(P1, JFK)'), expr('At(P1, ATL)'),
		expr('At(P2, SFO)'), expr('At(P2, ATL)'),
		expr('At(P3, JFK)'), expr('At(P3, SFO)')
	]
	init = FluentState(pos, neg)
	goal = [expr('At(C1, JFK)'), expr('At(C2, SFO)'), expr('At(C3, SFO)')]
	return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p3() -> AirCargoProblem:

	cargos   = [ 'C1',  'C2',  'C3',  'C4']
	planes   = [ 'P1',  'P2']
	airports = ['JFK', 'SFO', 'ATL', 'ORD']
	pos = [
		expr('At(C1, SFO)'), expr('At(C2, JFK)'), expr('At(C3, ATL)'), expr('At(C4, ORD)'),
		expr('At(P1, SFO)'), expr('At(P2, JFK)')
	]
	neg = [
		expr('At(C1, JFK)'), expr('At(C1, ATL)'), expr('At(C1, ORD)'), expr('In(C1, P1)'), expr('In(C1, P2)'),
		expr('At(C2, SFO)'), expr('At(C2, ATL)'), expr('At(C2, ORD)'), expr('In(C2, P1)'), expr('In(C2, P2)'),
		expr('At(C3, SFO)'), expr('At(C3, JFK)'), expr('At(C3, ORD)'), expr('In(C3, P1)'), expr('In(C3, P2)'),
		expr('At(C4, SFO)'), expr('At(C4, JFK)'), expr('At(C4, ATL)'), expr('In(C4, P1)'), expr('In(C4, P2)'),
		expr('At(P1, JFK)'), expr('At(P1, ATL)'), expr('At(P1, ORD)'),
		expr('At(P2, SFO)'), expr('At(P2, ATL)'), expr('At(P2, ORD)')
	]
	init = FluentState(pos, neg)
	goal = [ expr('At(C1, JFK)'), expr('At(C3, JFK)'), expr('At(C2, SFO)'), expr('At(C4, SFO)') ]
	return AirCargoProblem(cargos, planes, airports, init, goal)
