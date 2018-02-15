
import keras
import numpy as np

from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):

	# containers for input/output pairs
	X, y = [], []

	# iter
	for i in range(len(series) - window_size):

		X.append(series[i : i+window_size])
		y.append(series[i+window_size])

	# reshape each
	X, X.shape = np.asarray(X), (np.shape(X)[0:2])
	y, y.shape = np.asarray(y), (len(y), 1)

	return X, y



# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):

	model = Sequential()
	model.add(LSTM(5, input_shape=(window_size, 1)))
	model.add(Dense(1))

	return model



### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
	
	chars = list(set(text))
	punctuation = ['!', ',', '.', ':', ';', '?']
	alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

	for i in chars:

		if i in alphabet_upper:
			text = text.replace(i, i.lower())
		elif i in alphabet_lower:
			pass
		elif i not in punctuation:
			text = text.replace(i, " ")

	while "  " in text:
		text = text.replace("  ", " ")

	return text



### TODO: fill out the function below that transforms the input text and
### window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):

	# containers for input/output pairs
	inputs, outputs = [], []

	# iteratively slide the window-size over the input series 
	# to generate input/output pairs with each move being of 
	# length step_size
	for i in range(0, len(text)-window_size, step_size):
		
		inputs.append(text[i : i + window_size])
		outputs.append(text[i + window_size])

	return inputs,outputs



# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):

	model = Sequential()
	model.add(LSTM(200, input_shape = (window_size, num_chars)))
	model.add(Dense(num_chars,activation = 'softmax'))

	return model


