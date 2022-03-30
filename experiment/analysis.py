import matplotlib.pyplot as plt
import pandas as pd

FILENAME = "csv/results.csv"


def speedups():
	df = pd.read_csv(FILENAME)

	df["TimeSU"] = df["Time"] / df["TimeCR"]
	df["InfsSU"] = df["Infs"] / df["InfsCR"]

	print("Time SU:", df["TimeSU"].mean())
	print("INfs SU:", df["InfsSU"].mean())

	df.to_csv(FILENAME)


def main(field="Infs"):
	df = pd.read_csv(FILENAME)

	rates = df["Rate"].unique()
	sizes = df['Size'].unique()
	x = [i for i in range(len(sizes))]
	y = None

	plt.figure()
	plt.xticks(x, sizes)
	plt.xlabel("Infrastructure Size")
	plt.ylabel(field)
	for r in rates:
		y = df.loc[df["Rate"] == r][field]
		lbl = str(r*100) + "%"
		plt.plot(x, y, marker='o', label=lbl)
	plt.legend(loc="upper left")

	# axes = plt.gca()
	# axes.set_ylim([0, 220000])
	plt.savefig("../img/{}.png".format(field.lower()), dpi=600)
	plt.show()

	print("Plotted {}".format(field))


if __name__ == '__main__':
	main(field="Infs")
