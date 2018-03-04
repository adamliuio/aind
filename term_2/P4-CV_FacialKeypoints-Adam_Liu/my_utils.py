import os
import pandas as pd
import matplotlib.pyplot as plt


def show_model_graph(hist, save_name):

	choices = ["acc", "val_acc", "loss", "val_loss"]
	plt.figure(figsize=(16, 6))

	for i in range(2):

		if i == 0:
			plt.subplot(121)
			plt.plot(hist.history[choices[0]], label=choices[0])
			plt.plot(hist.history[choices[1]], label=choices[1])
			plt.title("Accuracy")
			plt.legend()

		if i == 1:
			plt.subplot(122)
			plt.plot(hist.history[choices[2]], label=choices[2])
			plt.plot(hist.history[choices[3]], label=choices[3])
			plt.title("Loss")
			plt.legend()

	plt.show()
	plt.savefig(save_name)



def show_csv_result(csv, save_name=None, training=False):

	hist = pd.read_csv(csv)
	choices = ["acc", "val_acc", "loss", "val_loss"]
	plt.figure(figsize=(16, 6))

	for i in range(2):

		if i == 0:
			plt.subplot(121)
			plt.plot(hist[choices[0]], label=choices[0])
			plt.plot(hist[choices[1]], label=choices[1])
			plt.title("Accuracy")
			plt.legend()

		if i == 1:
			plt.subplot(122)
			plt.plot(hist[choices[2]], label=choices[2])
			plt.plot(hist[choices[3]], label=choices[3])
			plt.title("Loss")
			plt.legend()

	plt.show()
	if training:
		if save_name == None:
			raise Exception("Need to have a name for the graph in training.")
		plt.savefig(save_name)

	f = pd.read_csv(csv)
	f = f.to_dict()

	max = 0

	for i in f["epoch"]:
		if f["val_acc"][i] > max:
			max = f["val_acc"][i]
			max_i = i

	return {
		'acc':      f['acc'     ][i],
		'loss':     f['loss'    ][i],
		'val_acc':  f['val_acc' ][i],
		'val_loss': f['val_loss'][i]
	}



def use_folder(path):    

	if path[-1] != "/":
		folder = "/".join(path.split("/")[:-1])

	else:
		folder = path

	if os.path.exists(folder) == False:
		os.makedirs(folder)

	return path