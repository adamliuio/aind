from aimacode.utils import expr
from aimacode.logic import associate


"""
	state object for planning problems as positive and negative fluents
"""
class FluentState():

	def __init__(self, pos_list, neg_list):
		self.pos = pos_list
		self.neg = neg_list

	def sentence(self):
		return expr(conjunctive_sentence(self.pos, self.neg))

	def pos_sentence(self):
		return expr(conjunctive_sentence(self.pos, []))


"""
	returns expr conjuntive sentence given positive and negative fluent lists

	:param pos_list: list of fluents
	:param neg_list: list of fluents
	:return: expr sentence of fluent conjunction
		e.g. "At(C1, SFO) ∧ ~At(P1, SFO)"
"""
def conjunctive_sentence(pos_list, neg_list):

	clauses = []
	for f in pos_list:
		clauses.append(expr("{}".format(f)))
	for f in neg_list:
		clauses.append(expr("~{}".format(f)))

	return associate('&', clauses)


"""
	encode fluents to a string of T/F using mapping

	:param fs: FluentState object
	:param fluent_map: ordered list of possible fluents for the problem
	:return: str eg. "TFFTFT" string of mapped positive and negative fluents
"""
def encode_state(fs: FluentState, fluent_map: list) -> str:

	state_tf = []
	for fluent in fluent_map:
		if fluent in fs.pos:
			state_tf.append('T')
		else:
			state_tf.append('F')

	return "".join(state_tf)


"""
	decode string of T/F as fluent per mapping

	:param state: str eg. "TFFTFT" string of mapped positive and negative fluents
	:param fluent_map: ordered list of possible fluents for the problem
	:return: fs: FluentState object

	lengths of state string and fluent_map list must be the same
"""
def decode_state(state: str, fluent_map: list) -> FluentState:
	fs = FluentState([], [])
	for idx, char in enumerate(state):
		if char == 'T':
			fs.pos.append(fluent_map[idx])
		else:
			fs.neg.append(fluent_map[idx])
	return fs
