
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import MaxPooling2D
from keras.layers import GlobalAveragePooling2D

from keras.models import Sequential


def get_model(model_name):

	if model_name == "model_1":

		model = Sequential()

		model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu', input_shape=(96, 96, 1)))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.1))

		model.add(Conv2D(filters=32, kernel_size=(2, 2), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.2))

		model.add(Conv2D(filters=64, kernel_size=(2, 2), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.3))

		model.add(Flatten())
		model.add(Dense(256, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(30))


	elif model_name == "model_2":

		model = Sequential()

		model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(96, 96, 1)))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.1))

		model.add(Conv2D(filters=64, kernel_size=(2, 2), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.2))

		model.add(Conv2D(filters=128, kernel_size=(2, 2), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.3))

		model.add(Flatten())
		model.add(Dense(1000, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(1000, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(30, activation='tanh'))


	elif model_name == "model_3":

		model = Sequential()

		model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(96, 96, 1)))
		model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))
		model.add(Dropout(0.1))

		model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
		model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
		model.add(Dropout(0.2))

		model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
		model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
		model.add(Dropout(0.3))

		model.add(Flatten())
		model.add(Dense(30, activation='tanh'))


	else:
		raise Exception("The model you chose is not defined.")


	return model




