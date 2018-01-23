
import keras
from keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

import numpy as np
import matplotlib.pyplot as plt

x_train = x_train.astype("float32") / 255
x_test  = x_test.astype("float32") / 255

from keras.utils import np_utils

num_classes = len(np.unique(y_train))
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test  = keras.utils.to_categorical(y_test,  num_classes)

x_train, x_valid = x_train[5000:], x_train[:5000]
y_train, y_valid = y_train[5000:], y_train[:5000]

print("x_train shape: %s" % str(x_train.shape))
print("y_train shape: %s" % str(y_train.shape))
print("x_test  shape: %s" % str( x_test.shape))
print("y_test  shape: %s" % str( y_test.shape))
print("x_valid shape: %s" % str(x_valid.shape))
print("y_valid shape: %s" % str(y_valid.shape))

from keras.models import Sequential
from keras.layers import Conv1D, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Reshape


model = Sequential()
model.add(Conv2D(filters=32, kernel_size=2, padding="same", activation="relu", input_shape=(32, 32, 3)))
model.add(Conv2D(filters=32, kernel_size=2, padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=64, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.1))
model.add(Conv2D(filters=64, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.1))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=96, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.2))
model.add(Conv2D(filters=96, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.2))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=128, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.3))
model.add(Conv2D(filters=128, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.3))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=160, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.4))
model.add(Conv2D(filters=160, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.4))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=192, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.5))
model.add(Conv2D(filters=192, kernel_size=2, padding="same", activation="relu"))
model.add(Dropout(.5))

model.add(Reshape((-1, 192)))

model.add(Conv1D(filters=10, kernel_size=1, padding="same", activation="relu"))


model.add(Flatten())
model.add(Dense(500, activation="relu"))
model.add(Dropout(.4))
model.add(Dense(10, activation="softmax"))

model.summary()

from keras.utils import plot_model
plot_model(model, to_file='./model.png')

model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

from time import time
from keras.callbacks import ModelCheckpoint

checkpointer = ModelCheckpoint(filepath="model_origin.weights.best.hdf5", verbose=1, save_best_only=True)

starttime = time()

hist = model.fit(x_train, y_train,
                 batch_size=32, epochs=100,
                 validation_data=(x_valid, y_valid),
                 callbacks=[checkpointer], verbose=2, shuffle=True)

print("time spent: %s" % time() - starttime)


model.load_weights("model_trying.weights.best.hdf5")

score = model.evaluate(x_test, y_test, verbose=0)
print('Test accuracy:', score[1])

y_hat = model.predict(x_test)
cifar10_labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


fig = plt.figure(figsize=(20, 8))

for i, idx in enumerate(np.random.choice(x_test.shape[0], size=32, replace=False)):
    ax = fig.add_subplot(4, 8, i + 1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(x_test[idx]))
    pred_idx = np.argmax(y_hat[idx])
    true_idx = np.argmax(y_test[idx])
    ax.set_title("{} ({})".format(cifar10_labels[pred_idx],
                                  cifar10_labels[true_idx]),
                 color=("green" if pred_idx == true_idx else "red"))

fig.savefig("final_result.png")