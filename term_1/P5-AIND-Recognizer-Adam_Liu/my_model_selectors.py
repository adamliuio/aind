import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


'''
	base class for model selection (strategy design pattern)
'''
class ModelSelector(object):

	def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
				 n_constant=3, min_n_components=2, max_n_components=10, random_state=14, verbose=False):

		self.verbose = verbose
		self.this_word = this_word
		self.n_constant = n_constant
		self.words = all_word_sequences
		self.hwords = all_word_Xlengths
		self.random_state = random_state
		self.min_n_components = min_n_components
		self.max_n_components = max_n_components
		self.sequences = all_word_sequences[this_word]
		self.X, self.lengths = all_word_Xlengths[this_word]


	def select(self):
		raise NotImplementedError


	def base_model(self, num_states):

		# with warnings.catch_warnings():
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# warnings.filterwarnings("ignore", category=RuntimeWarning)
		try:
			hmm_model = GaussianHMM(n_components=num_states,
									covariance_type="diag",
									n_iter=1000,
									random_state=self.random_state,
									verbose=False).fit(self.X, self.lengths)
			if self.verbose:
				print("model created for {} with {} states".format(self.this_word, num_states))
			return hmm_model

		except:
			if self.verbose:
				print("failure on {} with {} states".format(self.this_word, num_states))
			return None



"""
	select the model with value self.n_constant
"""
class SelectorConstant(ModelSelector):

	def select(self):
		""" select based on n_constant value

		:return: GaussianHMM object
		"""
		best_num_components = self.n_constant
		return self.base_model(best_num_components)



"""
	select the model with the lowest Bayesian Information Criterion(BIC) score

	http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
	Bayesian information criteria: BIC = -2 * logL + p * logN

		L: likelihood

		p: number of free parameters. It is the sum of
		1). The free transition probability parameters, which is the size of the
			transmat matrix less one row because they add up to 1 and therefore
			the final row is deterministic, so `n*(n-1)`;
		2). The free starting probabilities, which is the size of startprob minus
			1 because it adds to 1.0 and last one can be calculated so `n-1`;
		3). Number of means, which is `n*f`; 4). Number of covariances which is
			the size of the covars matrix, which for "diag" is `n*f`

		N: number of features
"""
class SelectorBIC(ModelSelector):

	"""
		select the best model for self.this_word based on
		BIC score for n between self.min_n_components and self.max_n_components

		:return: GaussianHMM object
	"""
	def select(self):
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# implement model selection based on BIC scores
		best_score, best_model  = float("inf"), None
		N, features_num = self.X.shape

		# loop over all valid n_components
		for components_num in range(self.min_n_components, self.max_n_components):

			try:
				# training the model
				model = GaussianHMM(n_components=num_states,
									covariance_type="diag",
									n_iter=1000,
									random_state=self.random_state,
									verbose=False)
				model.fit(self.X, self.lengths)

				# logging the likelihood of the model
				logL  = model.score(self.X, self.lengths)

				# number of parameters
				# p = m^2 +2mf-1
				params_num = components_num ** 2 + 2 * features_num * components_num - 1
				# calculating BIC
				# BIC = -2 * logL + p * logN
				bic_score = -2 * logL + params_num * np.log(N)

				if bic_score < best_score:
					best_score, best_model = bic_score, model

			except Exception:
				continue

		if best_model is not None:
			return best_model

		else:
			return self.base_model(self.n_constant)


'''
	select best model based on Discriminative Information Criterion

	Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
	Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
	http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
	https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
	DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
		= log likelihood of the data belonging to model
			  - avg of anti log likelihood of data X and model M\
		= log(P(original word)) - average(log(P(other words)))
'''
class SelectorDIC(ModelSelector):

	def select(self):
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		other_words = []
		best_score, best_model = float("-inf"), None

		for word in self.words:
			if word != self.this_word:
				other_words.append(self.hwords[word])

		# loop over all valid n_components
		for components_num in range(self.min_n_components, self.max_n_components):

			try:
				model = self.base_model(components_num)
				logL = model.score(self.X, self.lengths)
			except Exception: 
				break

			logL_other_words = [model.score(word[0], word[1]) for word in other_words]
			# calculating DIC
			dic_score = logL - np.mean(logL_other_words)

			if dic_score > best_score:
				best_score = dic_score
				best_model = model

		if best_model is not None:
			return best_model
		else:
			return self.base_model(self.n_constant)


'''
	select best model based on average log Likelihood of cross-validation folds
'''
class SelectorCV(ModelSelector):

	def select(self):

		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# Implementing CV
		n_splits = 2
		# n_splits = min(len(self.sequences), 3)    # previous
		best_score, best_model = float("-inf"), None
		scores = []

		for components_num in range(self.min_n_components, self.max_n_components + 1):

			if (len(self.sequences) < n_splits): 
				break

			# Implementing k fold
			folds = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)

			for train_index, test_index in folds.split(self.sequences):
				X_train, lengths_train = combine_sequences(train_index, self.sequences)
				X_test,  lengths_test  = combine_sequences( test_index, self.sequences)
				self.X,  self.lengths  = X_train, lengths_train

				try:
					model = self.base_model(components_num)
					logL = model.score(X_test, lengths_test)
					scores.append(logL)

				except Exception:
					break

			logL_mean = np.mean(logL) if len(scores) > 0 else float("-inf")

			if logL_mean > best_score:
				best_score, best_model = logL_mean, model

		if best_model:
			return best_model
		else:
			return self.base_model(self.n_constant)


